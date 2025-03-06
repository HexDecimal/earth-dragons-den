"""Room database and types."""

from __future__ import annotations

from enum import IntEnum


class RoomType(IntEnum):
    """Enumerator of room types."""

    Unassigned = 0
    Treasury = 1
