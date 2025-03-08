"""Faction types."""

from __future__ import annotations

from enum import Enum


class Faction(Enum):
    """List of factions."""

    Player = "PlayerFaction"
    Hostile = "HostileFaction"
