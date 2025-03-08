"""Actor functions."""

from __future__ import annotations

import tcod.ecs

from game.action import Action  # noqa: TC001
from game.components import AI, Location
from game.faction import Faction  # noqa: TC001
from game.timesys import schedule


def spawn_actor(template: tcod.ecs.Entity, pos: Location, ai: Action, faction: Faction) -> tcod.ecs.Entity:
    """Spawn an new actor and return the spawned entity."""
    actor = template.instantiate()
    actor.components[Location] = pos
    actor.components[AI] = ai
    actor.tags |= {faction}
    schedule(actor, 0)
    return actor
