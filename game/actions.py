"""Common actions."""

from __future__ import annotations

import attrs
import tcod.ecs

from game.action import ActionResult, Success
from game.components import Location


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
        actor.components[Location] = dest
        return Success()
