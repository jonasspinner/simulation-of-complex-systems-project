from itertools import product

import numpy as np
from numpy.linalg import norm


def getDistances(visibility_matrix: np.ndarray, environment: np.ndarray, resolution: int) -> np.ndarray:
    """
    Parameters
    ----------
    visibility_matrix
        Holds all visibility maps corresponding to each positions in the environment
    environment
        Used for finding non zero element when initializing distanceMatrix
    resolution : int

    Returns
    -------
    distances : np.ndarray
        distances describes the distance to all states in a radius of 2m
        (this depends on visibility_matrix) from a given state.
    """

    # Look for a state in environment which is not a wall since those states in visibilityMatrix are empty
    # non_empty_pos = next(zip(*np.where(environment != TileType.WALL & environment != TileType.TABLE)))
    found = False
    while found == False:
        for j in range(5,np.shape(environment)[0]):
            for i in range(5,np.shape(environment)[1]): 
                if environment[j,i] != 0:
                    distances = np.full(np.shape(visibility_matrix[int(j),int(i)]), 1, dtype=float)
                    found = True
    # non_empty_pos

    local_width, local_height = distances.shape
    #local_width, local_height = visibility_matrix[non_empty_pos].shape
    assert(local_width > 0)
    assert(local_height > 0)

    distances = np.full((local_width, local_height), 1, dtype=float)

    # Calculate distances from the middle position of the matrix
    local_mid = (local_width // 2, local_height // 2)

    for local_pos in product(range(local_width), range(local_height)):
        # Distance in meters
        distances[local_pos] = norm(np.array(local_pos) - np.array(local_mid)) / (2 * resolution)

    return distances


def getDirectedSpread(visibility_matrix: np.ndarray, environment: np.ndarray, resolution: int) -> np.ndarray:
    """
    Parameters
    ----------
    visibility_matrix
        Holds all visibility maps corresponding to each positions in the environment
    environment
        Used for finding non zero element when initializing distanceMatrix
    directionToTable
        0 if table to the right of agent
        1 if table down of agent
        2 if table to the left of agent
        3 if table is up from the agent
    resolution
        Resolution parameter.
        Changes the resolution of the environmental map.

    Returns
    -------
    cone : np.ndarray
        Represent a cone shaped vision in the direction to the table. 
        Has values in [0,1].
        This matrix is later multiplied with the particle spread matrix corresponding 
        to current time step in order to decrease backward spread. 
    """
    
    #non_empty_pos = next(zip(*np.where(environment != TileType.WALL & environment != TileType.TABLE)))

    #local_width, local_height = visibility_matrix[non_empty_pos].shape
    
    found = False
    while found == False:
        for j in range(5,np.shape(environment)[0]):
            for i in range(5,np.shape(environment)[1]): 
                if environment[j,i] != 0:
                    distances = np.full(np.shape(visibility_matrix[int(j),int(i)]), 1, dtype=float)
                    found = True

    local_width, local_height = distances.shape
    
    
    assert(local_width > 0)
    assert(local_height > 0)
        
    radius = 4*resolution
    radii = np.linspace(0, radius, 30)
    thetas = np.linspace(-np.pi, 0, 40)
    cone = np.zeros((radius*2 + 1, radius*2 + 1), dtype=float)
    
    for theta in thetas:
            for rad in radii:
                # Center of visibility calculation in local coordinates.
                local_x = radius
                local_y = radius

                # 0.5 since radius does not take in account that indexing starts at 0
                
                dx = int(0.5 + np.cos(theta) * rad)
                dy = int(np.floor(0.5 + np.sin(theta) * rad)) # np.floor since int() rounds up negative numbers
                assert(-radius <= dx <= radius)
                assert(-radius <= dy <= radius)

                if cone[local_x + dx, local_y + dy] < 0.01:
                    if np.cos(theta) < -0.75:
                        cone[local_x + dx, local_y + dy] = 0.1
                    else:    
                        cone[local_x + dx - 1, local_y + dy] = 5/8 + (3/8 * np.cos(theta))
                        
                dx = int(0.5 + np.cos(-theta) * rad)
                dy = int(0.5 + np.sin(-theta) * rad)
                assert(-radius <= dx <= radius)
                assert(-radius <= dy <= radius)
                
                if cone[local_x + dx, local_y + dy] < 0.01:
                    if np.cos(-theta) < -0.75:
                        cone[local_x + dx, local_y + dy] = 0.1
                    else:    
                        cone[local_x + dx - 1, local_y + dy] = 5/8 + (3/8 * np.cos(-theta))
    
    
    cones = np.zeros((1, 4), dtype=object)
    cones[0,0] = cone
    cones[0,1] = np.rot90(cone)
    cones[0,2] = np.rot90(cone,2)
    cones[0,3] = np.rot90(cone,3)
    return cones
    