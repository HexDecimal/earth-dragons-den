"""Movement handing functions."""

from __future__ import annotations

from collections.abc import Iterator

from tcod.ecs import Entity

from game.components import Location, Offset, Shape, TilesLayer
from game.tags import FacetOf, IsActor
from game.tile import TileDB


def in_bounds(pos: Location) -> bool:
    """Return True if a location is in bounds of its own map."""
    shape = pos.map.components[Shape]
    return 0 <= pos.x < shape.width and 0 <= pos.y < shape.height


def iter_entity_locations(entity: Entity, position: Location | None = None) -> Iterator[Location]:
    """Iterate over this entities locations.

    Defaults to the entities actual position, but `position` can be provided manually.
    """
    facets = entity.registry.Q.all_of(relations=[(FacetOf, entity)])
    if position is None:
        position = entity.components[Location]
    if not facets:
        yield position
        return
    yield from (position + facet.components[Offset] for facet in facets)


def check_move(entity: Entity, dest: Location, *, allow_dig: bool) -> int | None:
    """Return the cost to move to a tile, or None if a tile can not be moved to."""
    tile_db = entity.registry[None].components[TileDB]
    dest_tile = dest.map.components[TilesLayer].item(dest.ij)
    assert isinstance(dest_tile, int)
    costs = []
    for facet_dest in iter_entity_locations(entity, dest):
        if not in_bounds(facet_dest):
            continue
        dest_tile = dest.map.components[TilesLayer].item(facet_dest.ij)
        cost = tile_db.data["move_cost"].item(dest_tile) or (allow_dig and tile_db.data["dig_cost"].item(dest_tile))
        assert isinstance(cost, int)
        if cost == 0:
            return None  # Tile is solid
        for e in entity.registry.Q.all_of(tags=[facet_dest, IsActor]):
            if e is entity:
                continue  # No self collision
            if e.components[Location] == dest:
                return None  # Space occupied by actor
        for e in entity.registry.Q.all_of(
            tags=[facet_dest], relations=[(FacetOf, entity.registry.Q.all_of(tags=[IsActor]))]
        ):
            if e.relation_tag[FacetOf] is entity:
                continue  # No self collision
            if e.components[Location] == dest:
                return None  # Space occupied by multi-tile actor
        costs.append(cost)

    return max(costs)


def _touch_tile(dest: Location) -> None:
    """Touch/dig a tile."""
    if not in_bounds(dest):
        return
    tile_db = dest.map.registry[None].components[TileDB]
    dest_tile = dest.map.components[TilesLayer][dest.ij]
    if tile_db.data["dig_cost"][dest_tile]:
        dest.map.components[TilesLayer][dest.ij] = tile_db.names[str(tile_db.data["excavated_tile"][dest_tile])]


def force_move(entity: Entity, dest: Location) -> None:
    """Move an entity to a specific location."""
    _touch_tile(dest)
    entity.components[Location] = entity_pos = dest
    for facet in entity.registry.Q.all_of(relations=[(FacetOf, entity)]):
        facet.components[Location] = facet_pos = entity_pos + facet.components[Offset]
        _touch_tile(facet_pos)
