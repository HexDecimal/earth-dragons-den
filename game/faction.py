"""Faction types."""

from __future__ import annotations

from enum import Enum

import tcod.ecs


class Faction(Enum):
    """List of factions."""

    Player = "PlayerFaction"
    Hostile = "HostileFaction"


def is_enemy(actor: tcod.ecs.Entity, target: tcod.ecs.Entity) -> bool:
    """Return True if actor and target have different hostile factions."""
    my_factions = set(Faction).intersection(actor.tags)
    target_factions = set(Faction).intersection(target.tags)
    return my_factions != target_factions
