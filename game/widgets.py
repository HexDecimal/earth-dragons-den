"""Common widgets."""

from __future__ import annotations

from collections.abc import Callable, Sequence

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

from game.constants import DIR_KEYS, LABEL_COLOR, LABEL_SELECTED
from game.state import StateResult  # noqa: TC001
from game.widget import Widget, WidgetRenderInfo, WidgetSizeInfo


@attrs.define()
class Button:
    """Simple button."""

    label: str
    callback: Callable[[], StateResult]

    def on_event(self, event: tcod.event.Event, /) -> StateResult:
        """Handle button activation."""
        match event:
            case tcod.event.KeyDown(sym=KeySym.RETURN | KeySym.RETURN2 | KeySym.KP_ENTER):
                return self.callback()
            case _:
                return None

    def render(self, info: WidgetRenderInfo, /) -> None:
        """Render this widget."""
        fg, bg = LABEL_SELECTED if info.focus else LABEL_COLOR
        info.console.draw_rect(info.x, info.y, info.width, info.height, ch=0x20, fg=fg, bg=bg)
        info.console.print_box(info.x, info.y, info.width, info.height, f" {self.label}", fg=fg)

    def get_size(self, info: WidgetSizeInfo, /) -> tuple[int, int]:
        """Get the size of this widget."""
        return (info.max_width, tcod.console.get_height_rect(info.max_width, self.label))


@attrs.define()
class ListMenu:
    """Generic list menu."""

    items: Sequence[Widget]
    width: int = 30
    selected: int = 0

    def on_event(self, event: tcod.event.Event, /) -> StateResult:
        """Pass events to this widget."""
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS and DIR_KEYS[sym][1] != 0:
                _x, y = DIR_KEYS[sym]
                self.selected += y
                self.selected %= len(self.items)
                return None
            case _:
                return self.items[self.selected].on_event(event)

    def render(self, info: WidgetRenderInfo, /) -> None:
        """Render this widget."""
        height = len(self.items) + 2
        menu_console = tcod.console.Console(self.width - 2, height - 2)

        y = 0
        for i, item in enumerate(self.items):
            button_width, button_height = item.get_size(WidgetSizeInfo(self.width, 0))
            item.render(
                WidgetRenderInfo(
                    console=menu_console, x=0, y=y, focus=(i == self.selected), width=button_width, height=button_height
                ),
            )
            y += button_height

        info.console.draw_frame(info.x, info.y, self.width, height, fg=(255, 255, 255), bg=(0, 0, 0))
        menu_console.blit(info.console, info.x + 1, info.y + 1)

    def get_size(self, _info: WidgetSizeInfo, /) -> tuple[int, int]:
        """Get the size of this widget."""
        return (self.width, len(self.items))
