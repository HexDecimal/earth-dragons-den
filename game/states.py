"""Common game states."""

from __future__ import annotations

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
from game.menus import main_menu
from game.rendering import render_world
from game.room import RoomType
from game.state import State  # noqa: TC001
from game.tags import InStorage, IsPlayer
from game.timesys import Tick


@attrs.define()
class InGame:
    """Player in control state."""

    def on_event(self, event: tcod.event.Event) -> State:
        """State event handler."""
        (player,) = g.registry.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS:
                do_action(player, Bump(DIR_KEYS[sym]))
            case tcod.event.KeyDown(sym=sym) if sym in WAIT_KEYS:
                do_action(player, idle)
            case tcod.event.KeyDown(sym=KeySym.t):
                do_action(player, StampRoom(RoomType.Treasury))
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return main_menu(self)

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
