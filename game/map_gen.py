"""Map generator tools."""

from __future__ import annotations

from random import Random

import numpy as np
import tcod.ecs

from game.components import Shape, TilesArray
from game.tile import TileDB


def generate_cave_map(registry: tcod.ecs.Registry) -> tcod.ecs.Entity:
    """Return a new cave map."""
    rng = registry[None].components[Random]
    tile_db = registry[None].components[TileDB]
    map_ = registry[object()]
    map_.components[Shape] = shape = Shape(128, 128)
    map_.components[TilesArray] = tiles = np.zeros(shape, dtype=np.uint8)
    tiles[:] = tile_db.names["bedrock"]
    tiles[1:-1, 1:-1] = tile_db.names["rock wall"]
    for y in range(0, 128, 16):
        for x in range(0, 128, 16):
            width = rng.randint(4, 14)
            height = rng.randint(4, 14)
            left = x + rng.randint(1, 16 - width - 1)
            top = y + rng.randint(1, 16 - height - 1)
            tiles[top : top + height, left : left + width] = tile_db.names["rock floor"]

    return map_
