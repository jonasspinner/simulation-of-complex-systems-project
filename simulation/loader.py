from enum import IntEnum, unique, auto
from typing import Tuple, Mapping, List

import numpy as np

Pos = Tuple[int, int]


@unique
class TileType(IntEnum):
    WALL = auto()
    FLOOR = auto()
    SEAT = auto()
    ENTRY = auto()
    FOOD = auto()


TILE_MAP: Mapping[str, TileType] = {
    " ": TileType.FLOOR,
    "T": TileType.WALL,
    "C": TileType.SEAT,
    "X": TileType.WALL,
    "E": TileType.ENTRY,
    "F": TileType.FOOD
}


def load_environment(file_name: str, resolution: int) -> Tuple[np.ndarray, List[Pos], List[Pos], List[Pos]]:
    """
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

        matrix = np.zeros((height * resolution, width * resolution))
        positions: Mapping[TileType.Tile, List[Pos]] = {
            TileType.ENTRY: [], TileType.FOOD: [], TileType.SEAT: []
        }

        for i, cols in enumerate(rows):
            for j, character in enumerate(cols):
                row, col = i * resolution, j * resolution

                if character in TILE_MAP:
                    tile_type = TILE_MAP[character]
                    matrix[row:row + resolution, col:col + resolution] = tile_type

                    if tile_type in (TileType.ENTRY, TileType.FOOD, TileType.SEAT):
                        center = (row + resolution // 2, col + resolution // 2)
                        positions[tile_type].append(center)

        return matrix, positions[TileType.ENTRY], positions[TileType.FOOD], positions[TileType.SEAT]
