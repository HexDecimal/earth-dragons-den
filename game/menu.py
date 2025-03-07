"""Menu types."""

from __future__ import annotations

from collections.abc import Callable, Sequence

import attrs

from game.state import State  # noqa: TC001


@attrs.define()
class MenuItem:
    """Menu item."""

    label: str
    callback: Callable[[], State]


@attrs.define()
class Menu:
    """Menu controller."""

    items: Sequence[MenuItem]
    selected: int = 0
