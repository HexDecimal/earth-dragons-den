"""Actor functions."""

from __future__ import annotations

from collections.abc import Iterator

import tcod.ecs

from game.action import Action  # noqa: TC001
from game.components import AI, Location
from game.faction import Faction  # noqa: TC001
from game.tags import FacetOf, IsActor
from game.timesys import schedule


def spawn_actor(template: tcod.ecs.Entity, pos: Location, ai: Action, faction: Faction) -> tcod.ecs.Entity:
    """Spawn an new actor and return the spawned entity."""
    actor = template.instantiate()
    actor.components[Location] = pos
    actor.components[AI] = ai
    actor.tags |= {faction, IsActor}
    schedule(actor, 0)
    return actor


def actor_at(pos: Location) -> Iterator[tcod.ecs.Entity]:
    """Iterate over any actors at `pos`."""
    yield from pos.map.registry.Q.all_of(tags=[pos, IsActor]).none_of(relations=[(..., FacetOf, None)])
    # For facets, return the owning entity.
    for e in pos.map.registry.Q.all_of(tags=[pos], relations=[(FacetOf, ...)]).all_of(
        tags=[IsActor], traverse=[tcod.ecs.IsA, FacetOf]
    ):
        yield e.relation_tag[FacetOf]
