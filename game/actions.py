"""Common actions."""

from __future__ import annotations

import attrs
import tcod.ecs

from game.action import ActionResult, Impossible, Success
from game.components import Gold, Location
from game.tags import IsItem
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
        for pos in iter_entity_locations(actor):
            for item in actor.registry.Q.all_of(components=[Gold], tags=[IsItem, pos]):
                actor.components.setdefault(Gold, 0)
                actor.components[Gold] += item.components[Gold]
                item.clear()
        return Success()
