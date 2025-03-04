"""Movement handing functions."""

from __future__ import annotations

from tcod.ecs import Entity

from game.components import Location, TilesArray
from game.tile import TileDB


def check_move(entity: Entity, dest: Location) -> int | None:
    """Return the cost to move to a tile, or None if a tile can not be moved to."""
    tile_db = entity.registry[None].components[TileDB]
    dest_tile = dest.map.components[TilesArray][dest.ij]
    return tile_db.data["move_cost"].item(dest_tile) or tile_db.data["dig_cost"].item(dest_tile) or None


def force_move(entity: Entity, dest: Location) -> None:
    """Move an entity to a specific location."""
    tile_db = entity.registry[None].components[TileDB]
    dest_tile = dest.map.components[TilesArray][dest.ij]
    if tile_db.data["dig_cost"][dest_tile]:
        dest.map.components[TilesArray][dest.ij] = tile_db.names[str(tile_db.data["excavated_tile"][dest_tile])]
    entity.components[Location] = dest
