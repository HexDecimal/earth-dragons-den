"""Combat logic."""

from __future__ import annotations

import logging

import tcod.ecs

from game.action import ActionResult, Success
from game.components import AI, HP, Graphic, Str
from game.tags import IsActor
from game.timesys import Ticket

logger = logging.getLogger(__name__)


def attack_obj(actor: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
    """Attack a target."""
    logger.debug("%s attacks %s", actor, target)
    if HP in target.components:
        target.components[HP] -= actor.components[Str]
        if target.components[HP] <= 0:
            kill(target)
    return Success()


def kill(actor: tcod.ecs.Entity) -> None:
    """Kill an entity instantly."""
    actor.tags.remove(IsActor)
    actor.components[Graphic] = Graphic(ord("%"), (0x80, 0, 0))
    actor.components.pop(Ticket, None)
    actor.components.pop(AI, None)
