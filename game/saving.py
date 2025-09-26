"""Save and load functions."""

from __future__ import annotations

import lzma
import pickle
from pathlib import Path

import numpy as np
import tcod.ecs
from numpy.typing import NDArray

SAVE_DIR = Path("saves")
SAVE_PATH = SAVE_DIR / "save.sav.xz"


def save_world(registry: tcod.ecs.Registry) -> None:
    """Save the provided world to disk."""
    data = pickle.dumps(registry, protocol=5)
    data = lzma.compress(data)
    SAVE_DIR.mkdir(exist_ok=True)
    SAVE_PATH.write_bytes(data)


def load_world() -> tcod.ecs.Registry:
    """Return th perviously saved world."""
    data = SAVE_PATH.read_bytes()
    data = lzma.decompress(data)
    obj = pickle.loads(data)  # noqa: S301
    assert isinstance(obj, tcod.ecs.Registry)

    # Migrate old types
    for old_component, new_component in [
        (("TilesLayer", np.ndarray[tuple[int, ...], np.dtype[np.uint8]]), ("TilesLayer", NDArray[np.uint8])),
        (("RoomTypeLayer", np.ndarray[tuple[int, ...], np.dtype[np.uint8]]), ("RoomTypeLayer", NDArray[np.uint8])),
    ]:
        for entity in list(obj.Q.all_of(components=[old_component])):
            entity.components[new_component] = entity.components.pop(old_component)

    return obj
