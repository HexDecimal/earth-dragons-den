"""Tracked global names."""

from __future__ import annotations

import tcod.context
import tcod.ecs
import tcod.tileset

from game.state import State  # noqa: TC001

context: tcod.context.Context
"""Active tcod context."""

registry: tcod.ecs.Registry
"""Active ECS registry."""

state: State
"""Active game state."""

tileset: tcod.tileset.Tileset
"""Active tileset."""
