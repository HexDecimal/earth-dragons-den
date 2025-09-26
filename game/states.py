"""Common game states."""

from __future__ import annotations

import attrs
import tcod.console
import tcod.constants
import tcod.ecs
import tcod.event
import tcod.sdl.video
from tcod.event import KeySym

import g
from game.action_logic import do_action
from game.actions import Bump, MinionAI, StampRoom, idle
from game.actor_logic import spawn_actor
from game.components import Gold, Location
from game.constants import DIR_KEYS, WAIT_KEYS
from game.faction import Faction
from game.menus import main_menu
from game.rendering import render_world
from game.room import RoomType
from game.state import State, StateResult  # noqa: TC001
from game.tags import InStorage, IsPlayer
from game.timesys import Tick
from game.widget import Widget, WidgetRenderInfo, WidgetSizeInfo
from game.widgets import Button, ListMenu


@attrs.define()
class ModalState:
    """State with no real-time action."""

    def on_update(self) -> bool:
        """Do nothing."""
        return False


def _cast() -> StateResult:
    (player,) = g.registry.Q.all_of(tags=[IsPlayer])
    spawn_actor(player.registry["kobold"], player.components[Location], MinionAI(), Faction.Player)
    return InGame()


@attrs.define()
class InGame(ModalState):
    """Player in control state."""

    def on_event(self, event: tcod.event.Event) -> StateResult:  # noqa: PLR0911
        """State event handler."""
        (player,) = g.registry.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in DIR_KEYS:
                return do_action(player, Bump(DIR_KEYS[sym], allow_dig=True))
            case tcod.event.KeyDown(sym=sym) if sym in WAIT_KEYS:
                return do_action(player, idle)
            case tcod.event.KeyDown(sym=KeySym.T):
                return do_action(player, StampRoom(RoomType.Treasury))
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return UIState(self, main_menu(self))
            case tcod.event.KeyDown(sym=KeySym.SPACE):
                return GodMode()
            case tcod.event.KeyDown(sym=KeySym.Z):
                return UIState(self, ListMenu(items=[Button("Summon Kobold", _cast)]))

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

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """State event handler."""
        match event:
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return UIState(self, main_menu(self))
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
class UIState(ModalState):
    """Handle a UI widget or popup."""

    parent: State | None
    widget: Widget

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Pass event to widgets."""
        match event:
            case tcod.event.KeyDown(sym=KeySym.ESCAPE) | tcod.event.MouseButtonUp(button=tcod.event.MouseButton.RIGHT):
                return self.parent
            case _:
                return self.widget.on_event(event)

    def on_render(self, console: tcod.console.Console) -> None:
        """Render widgets."""
        if g.state == self and self.parent is not None:
            self.parent.on_render(console)
            console.rgb["fg"] //= 8
            console.rgb["bg"] //= 8

        width, height = self.widget.get_size(WidgetSizeInfo(max_width=console.width, max_height=console.height))
        self.widget.render(
            WidgetRenderInfo(
                console=console,
                x=console.width // 2 - width // 2,
                y=console.height // 2 - height // 2,
                width=width,
                height=height,
            )
        )
