"""Map generator tools."""

from __future__ import annotations

from random import Random

import attrs
import numpy as np
import tcod.ecs

from game.actions import GatherTreasureAI
from game.components import AI, Gold, Graphic, Location, RoomTypeLayer, Shape, TilesLayer
from game.tags import IsItem
from game.tile import TileDB
from game.timesys import schedule


@attrs.define
class Rect:
    """Generic rectangle."""

    x: int
    y: int
    width: int
    height: int

    @property
    def inner(self) -> tuple[slice, slice]:
        """Return inner area slice."""
        return slice(self.y, self.y + self.height), slice(self.x, self.x + self.width)


def generate_cave_map(registry: tcod.ecs.Registry) -> tcod.ecs.Entity:
    """Return a new cave map."""
    rng = registry[None].components[Random]
    tile_db = registry[None].components[TileDB]
    map_ = registry[object()]
    map_.components[Shape] = shape = Shape(128, 128)
    map_.components[TilesLayer] = tiles = np.zeros(shape, dtype=np.uint8)
    map_.components[RoomTypeLayer] = np.zeros(shape, dtype=np.uint8)
    tiles[:] = tile_db.names["bedrock"]
    tiles[1:-1, 1:-1] = tile_db.names["rock wall"]
    for y in range(0, 128, 16):
        for x in range(0, 128, 16):
            width = rng.randint(4, 14)
            height = rng.randint(4, 14)
            rect = Rect(x + rng.randint(1, 16 - width - 1), y + rng.randint(1, 16 - height - 1), width, height)
            tiles[rect.inner] = tile_db.names["rock floor"]
            for _ in range(2):
                obj = registry[object()]
                obj.components[Graphic] = Graphic(ord("$"))
                obj.components[Location] = Location(
                    x=rng.randint(rect.x, rect.x + rect.width - 1),
                    y=rng.randint(rect.y, rect.y + rect.height - 1),
                    map=map_,
                )
                obj.components[Gold] = rng.randint(10, 50)
                obj.tags.add(IsItem)
            obj = registry[object()]
            obj.components[Graphic] = Graphic(ord("k"))
            obj.components[Location] = Location(
                x=rng.randint(rect.x, rect.x + rect.width - 1),
                y=rng.randint(rect.y, rect.y + rect.height - 1),
                map=map_,
            )
            obj.components[AI] = GatherTreasureAI()
            schedule(obj, 0)

    return map_
