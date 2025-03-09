"""Common game states."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

import attrs
import tcod.console
import tcod.constants
import tcod.event
import tcod.sdl.video
from tcod.event import KeySym

import g
from game.action_logic import do_action
from game.actions import Bump, StampRoom, idle
from game.components import Gold
from game.constants import DIR_KEYS, WAIT_KEYS
from game.menu import Menu  # noqa: TC001
from game.menus import main_menu
from game.rendering import render_world
from game.room import RoomType
from game.state import State  # noqa: TC001
from game.tags import InStorage, IsPlayer
from game.timesys import Tick

T = TypeVar("T")


@attrs.define()
class ModalState:
    """State with no real-time action."""

    def on_update(self) -> bool:
        """Do nothing."""
        return False


@attrs.define()
class InGame(ModalState):
    """Player in control state."""

    def on_event(self, event: tcod.event.Event) -> State:
        """State event handler."""
        (player,) = g.registry.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS:
                do_action(player, Bump(DIR_KEYS[sym], allow_dig=True))
            case tcod.event.KeyDown(sym=sym) if sym in WAIT_KEYS:
                do_action(player, idle)
            case tcod.event.KeyDown(sym=KeySym.t):
                do_action(player, StampRoom(RoomType.Treasury))
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return MenuState(self, main_menu(self))
            case tcod.event.KeyDown(sym=KeySym.SPACE):
                return GodMode()

        return self

    def on_render(self, console: tcod.console.Console) -> None:
        """State rendering routine."""
        render_world(g.registry, console)

        (player,) = g.registry.Q.all_of(tags=[IsPlayer])
        console.print(0, 0, f"Gold: {player.components.get(Gold, 0)} ", fg=(255, 255, 255), bg=(0, 0, 0))
        console.print(0, 1, f"Tick: {g.registry[None].components.get(Tick, 0)} ", fg=(255, 255, 255), bg=(0, 0, 0))
        console.print(
            0,
            2,
            f"Gold store: {sum(e.components[Gold] for e in g.registry.Q.all_of(components=[Gold], tags=[InStorage]))} ",
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )


@attrs.define()
class GodMode:
    """Omniscient top-down view."""

    paused: bool = False

    def on_event(self, event: tcod.event.Event) -> State:
        """State event handler."""
        match event:
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return MenuState(self, main_menu(self))
            case tcod.event.KeyDown(sym=KeySym.SPACE):
                return InGame()
        return self

    def on_update(self) -> bool:
        """Auto advance time."""
        if not self.paused:
            (player,) = g.registry.Q.all_of(tags=[IsPlayer])
            do_action(player, idle)
            return True
        return False

    def on_render(self, console: tcod.console.Console) -> None:
        """Same rendering as InGame."""
        InGame().on_render(console)


@attrs.define()
class MenuState(ModalState):
    """Modal menu state."""

    parent: State | None
    menu: Menu[Callable[[], State]]

    def on_event(self, event: tcod.event.Event) -> State:
        """Handle menu events."""
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS:
                _x, y = DIR_KEYS[sym]
                self.menu.selected += y
                self.menu.selected %= len(self.menu.items)
            case tcod.event.KeyDown(sym=KeySym.RETURN | KeySym.RETURN2 | KeySym.KP_ENTER):
                return self.menu.items[self.menu.selected].value()
            case (
                tcod.event.KeyDown(sym=KeySym.ESCAPE) | tcod.event.MouseButtonDown(button=tcod.event.MouseButton.RIGHT)
            ):
                if self.parent is not None:
                    return self.parent
        return self

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the menu."""
        if g.state == self and self.parent is not None:
            self.parent.on_render(console)
            console.rgb["fg"] //= 8
            console.rgb["bg"] //= 8

        width = 30
        height = len(self.menu.items) + 2
        menu_console = tcod.console.Console(width, height)
        menu_console.draw_frame(0, 0, width, height)

        for i, item in enumerate(self.menu.items):
            fg = (0xFF, 0xFF, 0xFF) if i == self.menu.selected else (0x80, 0x80, 0x80)
            bg = (0x20, 0x20, 0x20) if i == self.menu.selected else None

            menu_console.print(2, i + 1, item.label, fg=fg, bg=bg)

        menu_console.blit(console, console.width // 2 - width // 2, console.height // 2 - height // 2)
