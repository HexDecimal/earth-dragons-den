"""Common game states."""

from __future__ import annotations

import attrs
import tcod.console
import tcod.event

import g
from game.action_logic import do_action
from game.actions import Bump
from game.rendering import render_world
from game.state import State  # noqa: TC001
from game.tags import IsPlayer

WAIT_KEYS = (
    tcod.event.KeySym.COMMA,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
)
DIR_KEYS = {
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.h: (-1, 0),
    tcod.event.KeySym.l: (1, 0),
    tcod.event.KeySym.k: (0, -1),
    tcod.event.KeySym.j: (0, 1),
    tcod.event.KeySym.y: (-1, -1),
    tcod.event.KeySym.b: (-1, 1),
    tcod.event.KeySym.u: (1, -1),
    tcod.event.KeySym.n: (1, 1),
}


@attrs.define()
class InGame:
    """State protocol."""

    def on_event(self, event: tcod.event.Event) -> State:
        """State event handler."""
        (player,) = g.registry.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS:
                do_action(player, Bump(DIR_KEYS[sym]))

        return self

    def on_render(self, console: tcod.console.Console) -> None:
        """State rendering routine."""
        render_world(g.registry, console)
