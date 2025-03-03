"""Common ECS components."""

from __future__ import annotations

from typing import Self

import attrs
import tcod.ecs


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
