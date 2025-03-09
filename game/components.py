"""Common ECS components."""

from __future__ import annotations

from typing import Final, NamedTuple, Self

import attrs
import numpy as np
import tcod.ecs
import tcod.ecs.callbacks
from numpy.typing import NDArray

from game.action import Action


@attrs.define(frozen=True)
class Graphic:
    """Entity glyph."""

    ch: int = ord("?")
    fg: tuple[int, int, int] = (255, 255, 255)

    def astuple(self) -> tuple[int, tuple[int, int, int]]:
        """Return attributes as a tuple."""
        return self.ch, self.fg


@attrs.define(frozen=True)
class Location:
    """Location component."""

    x: int
    y: int
    map: tcod.ecs.Entity

    def __add__(self, other: tuple[int, int]) -> Self:
        """Return a relative position by adding a vector."""
        x, y = other
        return self.__class__(self.x + x, self.y + y, self.map)

    @property
    def ij(self) -> tuple[int, int]:
        """Return the ij coordinates of this location."""
        return self.y, self.x

    def squared_distance(self, other: Location) -> int:
        """Return Euclidean distance squared between self and other."""
        return (self.x - other.x) * 2 + (self.y - other.y) * 2


class Shape(NamedTuple):
    """Shape of a map component."""

    height: int
    width: int


TilesLayer: Final = ("TilesLayer", NDArray[np.uint8])
"""Array of tile indexes."""

RoomTypeLayer: Final = ("RoomTypeLayer", NDArray[np.uint8])
"""Array of room type indexes."""


class Vector2(NamedTuple):
    """Generic X,Y vector."""

    x: int
    y: int


Offset: Final = ("Offset", Vector2)
"""Entity offset from parent position."""

Gold: Final = ("Gold", int)
"""Gold value."""


@tcod.ecs.callbacks.register_component_changed(component=Location)
def on_position_changed(entity: tcod.ecs.Entity, old: Location | None, new: Location | None) -> None:
    """Track entity positions as tags."""
    if old == new:
        return
    if old is not None:
        entity.tags.remove(old)
    if new is not None:
        entity.tags.add(new)


AI: Final = ("AI", Action)
"""AI for this entity/actor."""

HP: Final = ("HP", int)
"""Current git points."""
MaxHP: Final = ("MaxHP", int)
"""Maximum hit points"""

Str: Final = ("Str", int)
"""Entity strength."""

Name: Final = ("Name", int)
"""Entity name."""
