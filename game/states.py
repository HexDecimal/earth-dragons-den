"""Common game states."""

from __future__ import annotations

import attrs
import tcod.console
import tcod.event


@attrs.define()
class HelloWorld:
    """State protocol."""

    def on_event(self, event: tcod.event.Event) -> HelloWorld:
        """State event handler."""
        match event:
            case tcod.event.Quit():
                raise SystemExit
        return self

    def on_render(self, console: tcod.console.Console) -> None:
        """State rendering routine."""
        console.print(0, 0, "Hello World")
        console.rgb["bg"][::2, ::2] = 0x10
        console.rgb["bg"][1::2, 1::2] = 0x10
