"""Common menus."""

from __future__ import annotations

import g
import game.states
from game.action_logic import simulate
from game.state import State  # noqa: TC001
from game.widget import Widget  # noqa: TC001
from game.widgets import Button, ListMenu
from game.world_init import new_world


def new_game() -> State | None:
    """Start a new game."""
    g.registry = new_world()
    simulate(g.registry)
    return game.states.InGame()


def save_and_quit() -> State | None:
    """Raise system exit."""
    raise SystemExit


def main_menu(parent: State | None) -> Widget:
    """Return the main menu state."""
    items = [Button("New Game", new_game), Button("Save and Quit", save_and_quit)]
    if parent is not None:
        items.insert(0, Button("Continue", lambda: parent))
    return ListMenu(width=30, items=items)
