from typing import Tuple

import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb.
graphicDt = np.dtype(
    [
        ("ch", np.int32), # Unicode codepoint.
        ("fg", "3B"), # 3 unsigned bytes, for RGB colors
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data
tileDt = np.dtype(
    [
        ("walkable", np.bool), # True if walkable
        ("transparent", np.bool), # True if tile doesn't block FOV
        ("dark", graphicDt), # Graphics for when this tile is not in FOV
        ("light", graphicDt), # Graphics for when the tile is in FOV.
    ]
)

def newTile(
    *, # Enforce the use of keywords, so that parameter order doesn't matter
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tileDt)

# SHROUD respesents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphicDt)

floor = newTile(
    walkable=True,
    transparent=True,
    dark=(ord("#"), (19, 109, 21), (19, 109, 21)),
    light=(ord("#"), (65, 152, 10), (65, 152, 10)),
)

wall = newTile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)


