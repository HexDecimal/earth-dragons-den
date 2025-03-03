"""World initialization."""

from __future__ import annotations

import tcod.ecs

from game.components import Graphic, Location
from game.tags import IsPlayer


def new_world() -> tcod.ecs.Registry:
    """Return a newly created world."""
    registry = tcod.ecs.Registry()
    map_ = registry[object()]

    player = registry[object()]
    player.components[Location] = Location(0, 0, map_)
    player.components[Graphic] = Graphic(ord("@"))
    player.tags |= {IsPlayer}

    return registry
