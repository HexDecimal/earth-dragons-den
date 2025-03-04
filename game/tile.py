"""Tile data types."""

from __future__ import annotations

from collections.abc import Iterable

import attrs
import numpy as np


@attrs.define(frozen=True)
class Tile:
    """Data for a tile type."""

    name: str
    ch: int = ord("?")
    fg: tuple[int, int, int] = (255, 255, 255)
    bg: tuple[int, int, int] = (0, 0, 0)
    transparent: bool = False
    move_cost: int = 0
    dig_cost: int = 0
    excavated_tile: str = ""


TILE_DTYPE = np.dtype(
    [
        ("name", object),
        ("ch", int),
        ("fg", "3B"),
        ("bg", "3B"),
        ("transparent", bool),
        ("move_cost", np.int16),
        ("dig_cost", np.int16),
        ("excavated_tile", object),
    ]
)


class TileDB:
    """Database of tile data."""

    __slots__ = ("data", "names", "tiles")

    def __init__(self, tiles: Iterable[Tile] = ()) -> None:
        """Initialize the database."""
        self.tiles: list[Tile] = []
        self.names: dict[str, int] = {}
        self.data = np.zeros(256, dtype=TILE_DTYPE)

        for tile in tiles:
            self.assign(tile)

    def __getnewargs__(self) -> tuple[list[Tile]]:
        """Serialize this database via the Tile class."""
        return (self.tiles,)

    def assign(self, tile: Tile) -> None:
        """Assign a new tile."""
        assert tile.name not in self.names
        self.tiles.append(tile)
        index = len(self.tiles)
        self.names[tile.name] = index
        self.data[index] = attrs.astuple(tile)
