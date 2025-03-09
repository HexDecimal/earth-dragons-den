"""Actor functions."""

from __future__ import annotations

from collections.abc import Iterator

import numpy as np
import tcod.constants
import tcod.ecs
import tcod.map
from numpy.typing import NDArray

from game.action import Action  # noqa: TC001
from game.components import AI, HP, Location, MaxHP, TilesLayer
from game.faction import Faction  # noqa: TC001
from game.tags import FacetOf, IsActor
from game.tile import TileDB
from game.timesys import schedule


def spawn_actor(template: tcod.ecs.Entity, pos: Location, ai: Action, faction: Faction) -> tcod.ecs.Entity:
    """Spawn an new actor and return the spawned entity."""
    actor = template.instantiate()
    actor.components[Location] = pos
    actor.components[AI] = ai
    actor.tags |= {faction, IsActor}
    actor.components[HP] = actor.components[MaxHP]
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


def get_fov(actor: tcod.ecs.Entity) -> NDArray[np.bool_]:
    """Return the visible area of an actor."""
    tile_db = actor.registry[None].components[TileDB]
    transparency = tile_db.data["transparent"][actor.components[Location].map.components[TilesLayer]]
    return tcod.map.compute_fov(
        transparency, actor.components[Location].ij, algorithm=tcod.constants.FOV_SYMMETRIC_SHADOWCAST
    )
