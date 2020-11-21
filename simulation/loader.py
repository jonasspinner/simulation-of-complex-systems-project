import numpy as np

Tile = int

WALL: Tile = 0
FLOOR: Tile = 1
SEAT: Tile = 2
ENTRY: Tile = 3
FOOD: Tile = 4


def load_environment(file_name: str, resolution: int) -> np.ndarray:
    """
    Parameters
    ----------
    file_name : str
    resolution : int
        This decides how many squares each thing from the text file will be in the matrix
    """
    with open(file_name) as file:
        row = 0
        col = 0

        matrix = np.zeros((36*resolution, 60*resolution))

        conversion = {" ": FLOOR, "T": WALL, "C": SEAT, "X": WALL, "E": ENTRY, "F": FOOD}
        for line in file:
            for character in line:
                if character in conversion:
                    matrix[row:row+resolution, col:col+resolution] = conversion[character]
                col = col + resolution
            row = row + resolution
            col = 0

        return matrix
