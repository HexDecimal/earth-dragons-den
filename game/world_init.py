"""World initialization."""

from __future__ import annotations

import tcod.ecs

from game.components import Graphic, Location
from game.map_gen import generate_cave_map
from game.tags import IsPlayer
from game.tile import Tile, TileDB


def init_world(registry: tcod.ecs.Registry) -> None:
    """Initialize or reinitialize a world."""
    tile_db = registry[None].components.setdefault(TileDB, TileDB())
    tile_db.assign(Tile(name="bedrock", ch=ord("#")))
    tile_db.assign(Tile(name="dirt wall", ch=ord("-"), bg=(0x80, 0, 0), dig_cost=100, excavated_tile="dirt floor"))
    tile_db.assign(Tile(name="dirt floor", ch=ord("."), bg=(0x40, 0, 0), move_cost=100))
    tile_db.assign(
        Tile(name="rock wall", ch=ord("="), bg=(0x40, 0x40, 0x40), dig_cost=400, excavated_tile="rock floor")
    )
    tile_db.assign(Tile(name="rock floor", ch=ord("."), bg=(0x20, 0x20, 0x20), move_cost=100))


def new_world() -> tcod.ecs.Registry:
    """Return a newly created world."""
    registry = tcod.ecs.Registry()
    init_world(registry)

    map_ = generate_cave_map(registry)

    player = registry[object()]
    player.components[Location] = Location(1, 1, map_)
    player.components[Graphic] = Graphic(ord("@"))
    player.tags |= {IsPlayer}

    return registry
