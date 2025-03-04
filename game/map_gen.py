"""Map generator tools."""

from __future__ import annotations

import numpy as np
import tcod.ecs

from game.components import Shape, TilesArray
from game.tile import TileDB


def generate_cave_map(registry: tcod.ecs.Registry) -> tcod.ecs.Entity:
    """Return a new cave map."""
    tile_db = registry[None].components[TileDB]
    map_ = registry[object()]
    map_.components[Shape] = shape = Shape(128, 128)
    map_.components[TilesArray] = tiles = np.zeros(shape, dtype=np.uint8)
    tiles[:] = tile_db.names["bedrock"]
    tiles[1:-1, 1:-1] = tile_db.names["rock wall"]

    return map_
