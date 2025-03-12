"""UI widget types."""

from __future__ import annotations

from typing import Protocol

import attrs
import tcod.console
import tcod.event

from game.state import StateResult  # noqa: TC001


@attrs.define()
class WidgetSizeInfo:
    """Widget size negotiation info."""

    max_width: int
    max_height: int


@attrs.define()
class WidgetRenderInfo:
    """Widget rendering info."""

    console: tcod.console.Console
    x: int
    y: int
    width: int = 0
    height: int = 0
    focus: bool = True


class Widget(Protocol):
    """UI widget protocol."""

    def on_event(self, event: tcod.event.Event, /) -> StateResult:
        """Pass events to this widget."""
        ...

    def render(self, info: WidgetRenderInfo, /) -> None:
        """Render this widget."""
        ...

    def get_size(self, size_info: WidgetSizeInfo, /) -> tuple[int, int]:
        """Get the size of this widget."""
        ...
