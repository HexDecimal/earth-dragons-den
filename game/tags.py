"""Common ECS tags."""

from __future__ import annotations

from typing import Final

IsPlayer: Final = "IsPlayer"
"""Entity is the player character."""

FacetOf: Final = "FacetOf"
"""Entity represents a tile of a multi-tile target."""

IsItem: Final = "IsItem"
"""Entity is a small loose item."""

InStorage: Final = "InStorage"
"""Entity is in a stockpile."""

IsActor: Final = "IsActor"
"""Entity is a living character."""

IsIn: Final = "IsIn"
"""Is-in relation."""

IsSite: Final = "IsSite"
"""Entity is a site/map."""
