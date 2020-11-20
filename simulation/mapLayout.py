import numpy as np
row = 0
col = 0
resolution = 5 #This decides how many squares each thing from the text file will be in the matrix
file = open("map1")
iteratorRow = 0
iteratorCol = 0
matrix = np.zeros((36*resolution, 60*resolution))
for line in file:
    for character in line:
        if character == " ":
            while iteratorCol < resolution:
                while iteratorRow < resolution:
                    matrix[row + iteratorRow, col + iteratorCol] = 0
                    iteratorRow = iteratorRow +1
                iteratorCol = iteratorCol +1
                iteratorRow = 0

        if character == "T":
            while iteratorCol < resolution:
                while iteratorRow < resolution:
                    matrix[row + iteratorRow, col + iteratorCol] = 1
                    iteratorRow = iteratorRow +1
                iteratorCol = iteratorCol +1
                iteratorRow = 0

        if character == "C":
            while iteratorCol < resolution:
                while iteratorRow < resolution:
                    matrix[row + iteratorRow, col + iteratorCol] = 2
                    iteratorRow = iteratorRow +1
                iteratorCol = iteratorCol +1
                iteratorRow = 0

        if character == "X":
            while iteratorCol < resolution:
                while iteratorRow < resolution:
                    matrix[row + iteratorRow, col + iteratorCol] = 3
                    iteratorRow = iteratorRow +1
                iteratorCol = iteratorCol +1
                iteratorRow = 0

        if character == "E":
            while iteratorCol < resolution:
                while iteratorRow < resolution:
                    matrix[row + iteratorRow, col + iteratorCol] = 4
                    iteratorRow = iteratorRow +1
                iteratorCol = iteratorCol +1
                iteratorRow = 0

        if character == "F":
            while iteratorCol < resolution:
                while iteratorRow < resolution:
                    matrix[row + iteratorRow, col + iteratorCol] = 5
                    iteratorRow = iteratorRow +1
                iteratorCol = iteratorCol +1
                iteratorRow = 0

        col = col + resolution
        iteratorCol = 0
    row = row + resolution
    col = 0

print(matrix)
