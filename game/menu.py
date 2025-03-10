"""Menu types."""

from __future__ import annotations

from collections.abc import Sequence

import attrs


@attrs.define()
class MenuItem[T]:
    """Menu item."""

    label: str
    value: T


@attrs.define()
class Menu[T]:
    """Menu controller."""

    items: Sequence[MenuItem[T]]
    selected: int = 0
