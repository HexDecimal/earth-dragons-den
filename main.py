#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

import tcod.context
import tcod.event
import tcod.sdl.video
import tcod.tileset
from tcod.event import KeySym, Modifier

import g
from game.states import InGame
from game.world_init import new_world


def main() -> None:
    """Main entry point."""
    g.registry = new_world()
    g.state = InGame()
    tileset = tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)
    tcod.tileset.procedural_block_elements(tileset=tileset)
    with tcod.context.new(tileset=tileset, width=1280, height=720) as g.context:
        while True:
            console = g.context.new_console(40, 20)
            g.state.on_render(console)
            g.context.present(console, keep_aspect=False, integer_scaling=True)
            g.state.on_update()
            for event in tcod.event.get():
                match event:
                    case tcod.event.Quit():
                        raise SystemExit
                    case tcod.event.KeyDown(mod=mod, sym=KeySym.RETURN | KeySym.RETURN2 | KeySym.RETURN) if (
                        mod & Modifier.ALT
                    ):
                        sdl_window = g.context.sdl_window
                        assert sdl_window
                        if sdl_window.flags & tcod.sdl.video.WindowFlags.MAXIMIZED:
                            sdl_window.restore()
                        else:
                            sdl_window.maximize()
                    case _:
                        g.state = g.state.on_event(event)


if __name__ == "__main__":
    main()
