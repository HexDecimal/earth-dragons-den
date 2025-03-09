"""Common menus."""

from __future__ import annotations

from collections.abc import Callable

import g
import game.states
from game.menu import Menu, MenuItem
from game.state import State  # noqa: TC001
from game.world_init import new_world


def new_game() -> State:
    """Start a new game."""
    g.registry = new_world()
    return game.states.SiteSelect.new(None)


def save_and_quit() -> State:
    """Raise system exit."""
    raise SystemExit


def main_menu(parent: State | None) -> Menu[Callable[[], State]]:
    """Return the main menu state."""
    items = [MenuItem("New Game", new_game), MenuItem("Save and Quit", save_and_quit)]
    if parent is not None:
        items.insert(0, MenuItem("Continue", lambda: parent))
    return Menu(items)
