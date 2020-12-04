from enum import IntEnum, unique
from typing import Tuple, Mapping, List

import numpy as np

Pos = Tuple[int, int]


@unique
class TileType(IntEnum):
    WALL = 0
    FLOOR = 1
    SEAT = 2
    ENTRY = 3
    FOOD = 4
    ONEWAY_UP = 5
    ONEWAY_RIGHT = 6
    ONEWAY_DOWN = 7
    ONEWAY_LEFT = 8
    TABLE = 9
    WALKING_PATH = 10


TILE_MAP: Mapping[str, TileType] = {
    " ": TileType.FLOOR,
    "T": TileType.TABLE,
    "C": TileType.SEAT,
    "X": TileType.WALL,
    "E": TileType.ENTRY,
    "F": TileType.FOOD,
    "A": TileType.ONEWAY_UP,
    ">": TileType.ONEWAY_RIGHT,
    "V": TileType.ONEWAY_DOWN,
    "<": TileType.ONEWAY_LEFT,
    ".": TileType.WALKING_PATH
}


def load_environment(file_name: str, resolution: int) -> Tuple[np.ndarray, List[Pos], List[Pos], List[Pos]]:
    """
    Positions in for the environment are (x, y). The position (0, 0) is the top left position and (width-1, height-1) is
    the lower right position.

    Parameters
    ----------
    file_name : str
    resolution : int
        This decides how many squares each thing from the text file will be in the matrix

    Returns
    -------
    matrix : np.ndarray
    entries : List[Pos]
    foods : List[Pos]
    seats : List[Pos]
    """
    with open(file_name) as file:
        rows = [line.strip() for line in file]

    height, width = len(rows), max(len(row) for row in rows)

    if any(len(row) != width for row in rows):
        line_messages = [f"Line {i} ({len(row)} != {width}) \"{row}\""
                         for i, row in enumerate(rows) if len(row) != width]
        raise RuntimeError(f"Every row should have the same size. {' '.join(line_messages)}.")

    matrix = np.zeros((width * resolution, height * resolution), dtype=int)
    positions: Mapping[TileType.Tile, List[Pos]] = {
        TileType.ENTRY: [], TileType.FOOD: [], TileType.SEAT: []
    }

    for i, cols in enumerate(rows):
        for j, character in enumerate(cols):
            x = j * resolution
            y = i * resolution

            if character in TILE_MAP:
                tile_type = TILE_MAP[character]
                matrix[x:x + resolution, y:y + resolution] = tile_type

                if tile_type in (TileType.ENTRY, TileType.FOOD, TileType.SEAT):
                    center = (x + resolution // 2, y + resolution // 2)
                    positions[tile_type].append(center)

    return matrix, positions[TileType.ENTRY], positions[TileType.FOOD], positions[TileType.SEAT]
