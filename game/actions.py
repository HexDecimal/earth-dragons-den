"""Common actions."""

from __future__ import annotations

from collections import deque
from random import Random
from typing import Self

import attrs
import numpy as np
import tcod.ecs
import tcod.path
from numpy.typing import NDArray

from game.action import Action, ActionResult, Impossible, Success
from game.components import Gold, Graphic, Location, RoomTypeLayer, TilesLayer
from game.room import RoomType
from game.tags import InStorage, IsItem
from game.tile import TileDB
from game.travel import check_move, force_move, in_bounds, iter_entity_locations


def idle(_actor: tcod.ecs.Entity) -> Success:
    """Idle action."""
    return Success()


@attrs.define
class Bump:
    """Generic bump action."""

    dir: tuple[int, int]

    def __call__(self, actor: tcod.ecs.Entity) -> ActionResult:
        """Bump interaction."""
        dest = actor.components[Location] + self.dir
        if not in_bounds(dest):
            return Impossible("Out of bounds.")

        cost = check_move(actor, dest)
        if cost is None:
            return Impossible("Blocked.")
        force_move(actor, dest)
        map_room_types = dest.map.components[RoomTypeLayer]
        for pos in iter_entity_locations(actor):
            for item in actor.registry.Q.all_of(components=[Gold], tags=[IsItem, pos]).none_of(tags=[InStorage]):
                actor.components.setdefault(Gold, 0)
                actor.components[Gold] += item.components[Gold]
                item.clear()
            if (
                actor.components.get(Gold)
                and map_room_types[pos.ij] == RoomType.Treasury
                and not actor.registry.Q.all_of(components=[Gold], tags=[pos, InStorage])
            ):
                obj = actor.registry[object()]
                obj.components[Graphic] = Graphic(ord("$"))
                obj.components[Location] = pos
                obj.components[Gold] = actor.components[Gold]
                actor.components[Gold] = 0
                obj.tags.add(IsItem)
                obj.tags.add(InStorage)

        return Success()


def walk_random(actor: tcod.ecs.Entity) -> ActionResult:
    """Walk in a random direction."""
    rng = actor.registry[None].components[Random]
    dir_ = rng.choice(
        [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
    )
    return Bump(dir_)(actor)


@attrs.define
class StampRoom:
    """Assign room to this position."""

    set_room: RoomType

    def __call__(self, actor: tcod.ecs.Entity) -> ActionResult:
        """Bump interaction."""
        room_array = actor.components[Location].map.components[RoomTypeLayer]
        for pos in iter_entity_locations(actor):
            room_array[pos.ij] = self.set_room
        return Success()


@attrs.define
class FollowPath:
    """Follow path action."""

    path: deque[tuple[int, int]]

    @classmethod
    def from_ij_array(cls, array: NDArray[np.integer]) -> Self:
        """Initialize path from Numpy array."""
        return cls(deque((yx.item(1), yx.item(0)) for yx in array))

    def __call__(self, actor: tcod.ecs.Entity) -> ActionResult:
        """Take one step on path."""
        if not self.path:
            return Impossible("End of path reached.")
        dest_x, dest_y = self.path[0]
        actor_pos = actor.components[Location]
        result = Bump((dest_x - actor_pos.x, dest_y - actor_pos.y))(actor)
        if isinstance(result, Success):
            self.path.popleft()
        return result

    def __bool__(self) -> bool:
        """Falsy after path is fully traversed."""
        return bool(self.path)


def _get_graph(actor: tcod.ecs.Entity) -> tcod.path.SimpleGraph:
    """Return the pathfinding graph for an actor."""
    map_ = actor.components[Location].map
    tile_db = actor.registry[None].components[TileDB]
    return tcod.path.SimpleGraph(cost=tile_db.data["move_cost"][map_.components[TilesLayer]], cardinal=2, diagonal=3)


@attrs.define
class GatherTreasureAI:
    """Gather treasure AI."""

    sub_action: Action | None = None

    def __call__(self, actor: tcod.ecs.Entity) -> ActionResult:
        """Move to gather gold."""
        if self.sub_action:
            return self.sub_action(actor)
        actor_pos = actor.components[Location]
        if actor.components.get(Gold):  # Carry back gold.
            goal = actor_pos.map.components[RoomTypeLayer] == RoomType.Treasury
            if goal.any():
                pf = tcod.path.Pathfinder(_get_graph(actor))
                for i, j in np.argwhere(goal):
                    i = int(i)  # noqa: PLW2901
                    j = int(j)  # noqa: PLW2901
                    if actor.registry.Q.all_of(components=[Gold], tags=[InStorage, Location(j, i, actor_pos.map)]):
                        continue
                    pf.add_root((i, j))
                self.sub_action = FollowPath.from_ij_array(pf.path_from(actor_pos.ij)[1:])
                if self.sub_action:
                    return self.sub_action(actor)
        else:  # Find gold.
            pf = tcod.path.Pathfinder(_get_graph(actor))
            for e in actor.registry.Q.all_of([Gold, Location], tags=[IsItem]).none_of(tags=[InStorage]):
                pf.add_root(e.components[Location].ij)
            self.sub_action = FollowPath.from_ij_array(pf.path_from(actor_pos.ij)[1:])
            if self.sub_action:
                return self.sub_action(actor)

        return walk_random(actor)
