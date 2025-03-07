"""Common menus."""

from __future__ import annotations

import g
import game.states
from game.menu import MenuItem, MenuState
from game.state import State  # noqa: TC001
from game.world_init import new_world


def new_game() -> State:
    """Start a new game."""
    g.registry = new_world()
    return game.states.InGame()


def main_menu(parent: State | None) -> State:
    """Return the main menu state."""
    items = [MenuItem("New Game", new_game)]
    if parent is not None:
        items.insert(0, MenuItem("Continue", lambda: parent))
    return MenuState(parent, items)
