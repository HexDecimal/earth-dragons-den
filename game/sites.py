"""Site functions."""

from __future__ import annotations

import tcod.ecs

from game.components import Name
from game.tags import IsSite


def new_site(registry: tcod.ecs.Registry, name: str) -> tcod.ecs.Entity:
    """Make a new site."""
    site = registry[object()]
    site.tags.add(IsSite)
    site.components[Name] = name
    return site


def get_sites(registry: tcod.ecs.Registry) -> list[tcod.ecs.Entity]:
    """Return the list of known sites in order."""
    return sorted(registry.Q.all_of(tags=[IsSite]), key=lambda e: e.components[Name])
