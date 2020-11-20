import numpy as np
row = 0
col = 0

file = open("map1")

matrix = np.zeros((36, 60))
for line in file:
    for character in line:
        if character == " ":
            matrix[row, col] = 0
        if character == "T":
            matrix[row, col] = 1
        if character == "C":
            matrix[row, col] = 2
        if character == "X":
            matrix[row, col] = 3
        if character == "E":
            matrix[row, col] = 4
        if character == "F":
            matrix[row, col] = 5
        col = col + 1
    row = row + 1
    col = 0

print(matrix)
