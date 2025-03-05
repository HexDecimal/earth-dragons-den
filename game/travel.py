"""Movement handing functions."""

from __future__ import annotations

from tcod.ecs import Entity

from game.components import Location, Offset, Shape, TilesArray
from game.tags import FacetOf
from game.tile import TileDB


def in_bounds(pos: Location) -> bool:
    """Return True if a location is in bounds of its own map."""
    shape = pos.map.components[Shape]
    return 0 <= pos.x < shape.width and 0 <= pos.y < shape.height


def check_move(entity: Entity, dest: Location) -> int | None:
    """Return the cost to move to a tile, or None if a tile can not be moved to."""
    tile_db = entity.registry[None].components[TileDB]
    dest_tile: int = dest.map.components[TilesArray].item(dest.ij)
    facets = entity.registry.Q.all_of(relations=[(FacetOf, entity)])
    if not facets:
        return tile_db.data["move_cost"].item(dest_tile) or tile_db.data["dig_cost"].item(dest_tile) or None
    costs = []
    for facet in facets:
        facet_dest = dest + facet.components[Offset]
        if not in_bounds(facet_dest):
            continue
        dest_tile = dest.map.components[TilesArray].item(facet_dest.ij)
        cost: int = tile_db.data["move_cost"].item(dest_tile) or tile_db.data["dig_cost"].item(dest_tile)
        if cost == 0:
            return None
        costs.append(cost)
    return max(costs)


def _touch_tile(dest: Location) -> None:
    """Touch/dig a tile."""
    if not in_bounds(dest):
        return
    tile_db = dest.map.registry[None].components[TileDB]
    dest_tile = dest.map.components[TilesArray][dest.ij]
    if tile_db.data["dig_cost"][dest_tile]:
        dest.map.components[TilesArray][dest.ij] = tile_db.names[str(tile_db.data["excavated_tile"][dest_tile])]


def force_move(entity: Entity, dest: Location) -> None:
    """Move an entity to a specific location."""
    _touch_tile(dest)
    entity.components[Location] = entity_pos = dest
    for facet in entity.registry.Q.all_of(relations=[(FacetOf, entity)]):
        facet.components[Location] = facet_pos = entity_pos + facet.components[Offset]
        _touch_tile(facet_pos)
