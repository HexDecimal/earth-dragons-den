"""Action functions."""

from __future__ import annotations

import tcod.ecs

from game.action import Action, Impossible, Success


def do_action(actor: tcod.ecs.Entity, action: Action) -> None:
    """Apply an action and its side effects."""
    match action(actor):
        case Success():
            pass
        case Impossible(msg=msg):
            print(msg)
