"""Rendering functions."""

from __future__ import annotations

import tcod.camera
import tcod.console
import tcod.ecs

from game.components import Graphic, Location, Shape, TilesArray
from game.tags import IsPlayer
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
    console.rgb[screen_slice] = tile_db.data[["ch", "fg", "bg"]][map_.components[TilesArray][world_slice]]

    for entity in registry.Q.all_of(components=[Graphic, Location]):
        entity_pos = entity.components[Location]
        x = entity_pos.x - camera_x
        y = entity_pos.y - camera_y
        if 0 <= x < console.width and 0 <= y < console.height:
            sprite = entity.components[Graphic]
            console.rgb[["ch", "fg"]][y, x] = sprite.astuple()
