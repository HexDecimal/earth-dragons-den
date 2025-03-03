"""State types."""

from __future__ import annotations

from typing import Protocol

import tcod.console
import tcod.event


class State(Protocol):
    """State protocol."""

    def on_event(self, event: tcod.event.Event, /) -> State:
        """State event handler."""
        ...

    def on_render(self, console: tcod.console.Console, /) -> None:
        """State rendering routine."""
        ...
