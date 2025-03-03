"""Action functions."""

from __future__ import annotations

import tcod.ecs

from game.action import Action  # noqa: TC001


def do_action(actor: tcod.ecs.Entity, action: Action) -> None:
    """Apply an action and its side effects."""
    action(actor)
