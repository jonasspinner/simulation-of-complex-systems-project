from typing import Tuple, Mapping, List

import numpy as np

Tile = int
Pos = Tuple[int, int]

WALL: Tile = 0
FLOOR: Tile = 1
SEAT: Tile = 2
ENTRY: Tile = 3
FOOD: Tile = 4


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
        row = 0
        col = 0

        matrix = np.zeros((36 * resolution, 60 * resolution))
        positions: Mapping[Tile, List[Pos]] = {ENTRY: [], FOOD: [], SEAT: []}

        conversion = {" ": FLOOR, "T": WALL, "C": SEAT, "X": WALL, "E": ENTRY, "F": FOOD}
        for line in file:
            for character in line:
                if character in conversion:
                    tile_type = conversion[character]
                    matrix[row:row + resolution, col:col + resolution] = tile_type
                    if tile_type in (ENTRY, FOOD, SEAT):
                        positions[tile_type].append((row + resolution // 2, col + resolution // 2))
                col = col + resolution
            row = row + resolution
            col = 0

        return matrix, positions[ENTRY], positions[FOOD], positions[SEAT]
