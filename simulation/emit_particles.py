from itertools import product

import numpy as np
from numpy.linalg import norm

from loader import TileType


def getDistances(visibility_matrix: np.ndarray, environment: np.ndarray) -> np.ndarray:
    """
    Parameters
    ----------
    visibility_matrix
        Holds all visibility maps corresponding to each positions in the environment
    environment
        Used for finding non zero element when initializing distanceMatrix

    Returns
    -------
    distances : np.ndarray
        distances describes the distance to all states in a radius of 2m
        (this depends on visibility_matrix) from a given state.
    """

    # Look for a state in environment which is not a wall since those states in visibilityMatrix are empty
    non_empty_pos = next(zip(*np.where(environment != TileType.WALL & environment != TileType.TABLE)))

    local_width, local_height = visibility_matrix[non_empty_pos].shape
    assert(local_width > 0)
    assert(local_height > 0)

    distances = np.full((local_width, local_height), 1, dtype=float)

    # Calculate distances from the middle position of the matrix
    local_mid = (local_width // 2, local_height // 2)

    for local_pos in product(range(local_width), range(local_height)):
        if local_pos == local_mid:
            distances[local_pos] = 0.5
        else:
            distances[local_pos] = norm(np.array(local_pos) - np.array(local_mid))

    return distances
