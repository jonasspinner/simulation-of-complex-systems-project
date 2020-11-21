import numpy as np

def load_environment(fileName, resolution) -> np.ndarray:

    Tile = int

    WALL:  Tile = 0
    FLOOR: Tile = 1
    SEAT:  Tile = 2
    ENTRY: Tile = 3
    FOOD:  Tile = 4

    row = 0
    col = 0
    resolution = resolution #This decides how many squares each thing from the text file will be in the matrix
    file = open(fileName)
    iteratorRow = 0
    iteratorCol = 0
    matrix = np.zeros((36*resolution, 60*resolution))
    for line in file:
        for character in line:
            if character == " ":
                while iteratorCol < resolution:
                    while iteratorRow < resolution:
                        matrix[row + iteratorRow, col + iteratorCol] = FLOOR
                        iteratorRow = iteratorRow +1
                    iteratorCol = iteratorCol +1
                    iteratorRow = 0

            if character == "T":
                while iteratorCol < resolution:
                    while iteratorRow < resolution:
                        matrix[row + iteratorRow, col + iteratorCol] = WALL
                        iteratorRow = iteratorRow +1
                    iteratorCol = iteratorCol +1
                    iteratorRow = 0

            if character == "C":
                while iteratorCol < resolution:
                    while iteratorRow < resolution:
                        matrix[row + iteratorRow, col + iteratorCol] = SEAT
                        iteratorRow = iteratorRow +1
                    iteratorCol = iteratorCol +1
                    iteratorRow = 0

            if character == "X":
                while iteratorCol < resolution:
                    while iteratorRow < resolution:
                        matrix[row + iteratorRow, col + iteratorCol] = WALL
                        iteratorRow = iteratorRow +1
                    iteratorCol = iteratorCol +1
                    iteratorRow = 0

            if character == "E":
                while iteratorCol < resolution:
                    while iteratorRow < resolution:
                        matrix[row + iteratorRow, col + iteratorCol] = ENTRY
                        iteratorRow = iteratorRow +1
                    iteratorCol = iteratorCol +1
                    iteratorRow = 0

            if character == "F":
                while iteratorCol < resolution:
                    while iteratorRow < resolution:
                        matrix[row + iteratorRow, col + iteratorCol] = FOOD
                        iteratorRow = iteratorRow +1
                    iteratorCol = iteratorCol +1
                    iteratorRow = 0

            col = col + resolution
            iteratorCol = 0
        row = row + resolution
        col = 0

    return matrix