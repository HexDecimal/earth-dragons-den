#!/usr/bin/env python3
"""Main script."""

from __future__ import annotations

import tcod.context
import tcod.event
import tcod.tileset

import g
from game.states import InGame
from game.world_init import new_world


def main() -> None:
    """Main entry point."""
    g.registry = new_world()
    g.state = InGame()
    tileset = tcod.tileset.load_tilesheet("assets/terminal8x12_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)
    with tcod.context.new(tileset=tileset) as g.context:
        while True:
            console = g.context.new_console(40, 20)
            g.state.on_render(console)
            g.context.present(console, keep_aspect=False, integer_scaling=True)
            for event in tcod.event.wait():
                g.state = g.state.on_event(event)


if __name__ == "__main__":
    main()
