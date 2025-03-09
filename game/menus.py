"""Common menus."""

from __future__ import annotations

from collections.abc import Callable, Iterable

import g
import game.states
from game.action_logic import simulate
from game.menu import Menu, MenuItem
from game.state import State  # noqa: TC001
from game.world_init import new_world


def new_game() -> State | None:
    """Start a new game."""
    g.registry = new_world()
    simulate(g.registry)
    return game.states.InGame()


def save_and_quit() -> State | None:
    """Raise system exit."""
    raise SystemExit


def main_menu(parent: State | None) -> Menu[Callable[[], State | None]]:
    """Return the main menu state."""
    items = [MenuItem("New Game", new_game), MenuItem("Save and Quit", save_and_quit)]
    if parent is not None:
        items.insert(0, MenuItem("Continue", lambda: parent))
    return Menu(items)


def setup_menu[T](
    callback: Callable[[T], State | None], items: Iterable[MenuItem[T]]
) -> Menu[Callable[[], State | None]]:
    """Configure a menu to use a generic callback."""
    menu = [(MenuItem(item.label, lambda item=item: callback(item.value))) for item in items]
    return Menu(menu)  # type: ignore[arg-type]
