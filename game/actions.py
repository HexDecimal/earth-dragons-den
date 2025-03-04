"""Common actions."""

from __future__ import annotations

import attrs
import tcod.ecs

from game.action import ActionResult, Impossible, Success
from game.components import Location, Shape
from game.travel import check_move, force_move


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

        cost = check_move(actor, dest)
        if cost is None:
            return Impossible("Blocked.")
        force_move(actor, dest)
        return Success()
