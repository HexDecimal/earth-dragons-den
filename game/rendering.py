"""Rendering functions."""

from __future__ import annotations

from collections import defaultdict

import tcod.camera
import tcod.console
import tcod.ecs

from game.components import Graphic, Location, RoomTypeLayer, Shape, TilesLayer
from game.tags import FacetOf, IsActor, IsItem, IsPlayer
from game.tile import TileDB


def render_world(registry: tcod.ecs.Registry, console: tcod.console.Console) -> None:
    """Render the active scene onto the console."""
    (player,) = registry.Q.all_of(tags=[IsPlayer])
    tile_db = registry[None].components[TileDB]

    player_pos = player.components[Location]
    map_ = player_pos.map
    camera_y, camera_x = (player_pos.y - console.height // 2, player_pos.x - console.width // 2)

    screen_slice, world_slice = tcod.camera.get_slices(
        (console.height, console.width), map_.components[Shape], (camera_y, camera_x)
    )
    console.rgb[screen_slice] = tile_db.data[["ch", "fg", "bg"]][map_.components[TilesLayer][world_slice]]
    console.rgb[["ch", "fg"]][screen_slice][map_.components[RoomTypeLayer][world_slice] == 1] = (
        ord("t"),
        (0x40, 0x40, 0x40),
    )

    to_display = defaultdict[tuple[int, int], list[tuple[int, tcod.ecs.Entity]]](list)

    for entity in registry.Q.all_of(components=[Graphic, Location]):
        entity_pos = entity.components[Location]
        x = entity_pos.x - camera_x
        y = entity_pos.y - camera_y
        if 0 <= x < console.width and 0 <= y < console.height:
            order = 0
            if FacetOf in entity.relation_tag:
                order = 3
            elif IsActor in entity.tags:
                order = 2
            elif IsItem in entity.tags:
                order = 1
            to_display[(y, x)].append((order, entity))
    for yx, sprites in to_display.items():
        console.rgb[["ch", "fg"]][yx] = max(sprites, key=lambda it: it[0])[1].components[Graphic].astuple()
