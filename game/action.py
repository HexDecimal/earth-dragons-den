"""Action types."""

from __future__ import annotations

from typing import Protocol

import attrs
import tcod.ecs


class Action(Protocol):
    """Abstract action type."""

    def __call__(self, actor: tcod.ecs.Entity, /) -> ActionResult:
        """Perform this action and return the result."""
        ...


@attrs.define
class Success:
    """Successful action result."""


@attrs.define
class Impossible:
    """Action was unable to be performed."""

    msg: str


ActionResult = Success | Impossible
