"""Menu types."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Generic, TypeVar

import attrs

T = TypeVar("T")


@attrs.define()
class MenuItem(Generic[T]):
    """Menu item."""

    label: str
    value: T


@attrs.define()
class Menu(Generic[T]):
    """Menu controller."""

    items: Sequence[MenuItem[T]]
    selected: int = 0
