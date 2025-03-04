"""Common actions."""

from __future__ import annotations

import attrs
import tcod.ecs

from game.action import ActionResult, Impossible, Success
from game.components import Location, Shape, TilesArray
from game.tile import TileDB


def idle(_actor: tcod.ecs.Entity) -> Success:
    """Idle action."""
    return Success()


def _in_bounds(pos: Location) -> bool:
    """Return True if a location is in bounds of its own map."""
    shape = pos.map.components[Shape]
    return 0 <= pos.x < shape.width and 0 <= pos.y < shape.height


@attrs.define
class Bump:
    """Generic bump action."""

    dir: tuple[int, int]

    def __call__(self, actor: tcod.ecs.Entity) -> ActionResult:
        """Bump interaction."""
        dest = actor.components[Location] + self.dir
        if not _in_bounds(dest):
            return Impossible("Out of bounds.")

        tiles_db = actor.registry[None].components[TileDB]
        dest_tile = dest.map.components[TilesArray][dest.ij]
        if tiles_db.data["move_cost"][dest_tile] != 0:
            actor.components[Location] = dest
            return Success()
        if tiles_db.data["dig_cost"][dest_tile] != 0:
            dest.map.components[TilesArray][dest.ij] = tiles_db.names[str(tiles_db.data["excavated_tile"][dest_tile])]
            actor.components[Location] = dest
            return Success()

        return Impossible("Blocked.")
