"""Menu types."""

from __future__ import annotations

from collections.abc import Callable, Sequence

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import g
from game.constants import DIR_KEYS
from game.state import State  # noqa: TC001


@attrs.define()
class MenuItem:
    """Menu item."""

    label: str
    callback: Callable[[], State]


@attrs.define()
class MenuState:
    """Modal menu state."""

    parent: State | None
    menu: Sequence[MenuItem]
    selected: int = 0

    def on_event(self, event: tcod.event.Event) -> State:
        """Handle menu events."""
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS:
                _x, y = DIR_KEYS[sym]
                self.selected = (self.selected + y) % len(self.menu)
            case tcod.event.KeyDown(sym=KeySym.RETURN | KeySym.RETURN2 | KeySym.KP_ENTER):
                return self.menu[self.selected].callback()
        return self

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the menu."""
        if g.state is self and self.parent is not None:
            self.parent.on_render(console)
            console.rgb["fg"] //= 8
            console.rgb["bg"] //= 8

        for i, item in enumerate(self.menu):
            fg = (0xFF, 0xFF, 0xFF) if i == self.selected else (0x80, 0x80, 0x80)
            bg = (0x20, 0x20, 0x20) if i == self.selected else None

            console.print(0, i, item.label, fg=fg, bg=bg)
