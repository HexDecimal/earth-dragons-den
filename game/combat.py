"""Combat logic."""

from __future__ import annotations

import logging

import tcod.ecs

from game.action import ActionResult, Success

logger = logging.getLogger(__name__)


def attack_obj(actor: tcod.ecs.Entity, target: tcod.ecs.Entity) -> ActionResult:
    """Attack a target."""
    logger.debug("%s attacks %s", actor, target)
    return Success()
