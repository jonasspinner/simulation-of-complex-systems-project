import numpy as np
from simulation.loader import TileType


def getVisibilityMaps(environment: np.ndarray, resolution: int, screen: bool) -> np.ndarray:
    """
    Parameters
    ----------
    environment : matrix
        In correct dimensions, i.e resolution has already been applied
    resolution : int
        Use this for scale, i.e if we decide that one original square is 50x50 cm,
        then one square in the environment is 50/res x 50/res cm. Need this for 
        the radius of particle emission.
    screen : boolean
        if true, particles is not spread over tables (tables is then seen as screens)
    Returns
    -------
    matrix : np.ndarray
        Matrix with visibility matrices for all possible positions in environment. 
        1 for visible state (i.e a state to which particle emits from a given position)
        0 for non visible states.
    """
    width, height = environment.shape

    def calculate_local_visibility(col: int, row: int) -> np.ndarray:
        # how much is two meters? Assuming 1 (original) square in original map is 50 cm. 
        radius = 4*resolution 
        radii = np.linspace(0, radius, 30)
        thetas = np.linspace(0, 2*np.pi, 75)
        visibility_from_pos = 2 + np.zeros((radius*2 + 1, radius*2 + 1), dtype=int)
        
        for theta in thetas:
            for rad in radii:
                # Center of visibility calculation in local coordinates.
                local_x = radius
                local_y = radius

                # 0.5 since radius does not take in account that indexing starts at 0
                dx = int(0.5 + np.cos(theta) * rad)
                dy = int(0.5 + np.sin(theta) * rad)
                assert(-radius <= dx <= radius)
                assert(-radius <= dy <= radius)

                # Break if outside of map (case if entry/food is on boundary, this way food is enabled to be placed
                # anywhere in the map)
                if not (0 <= col + dx < width and 0 <= row + dy < height):
                    break

                tile_type = environment[col + dx, row + dy]

                
                if tile_type == TileType.WALL or (tile_type == TileType.TABLE and screen == True):
                    visibility_from_pos[local_x + dx, local_y + dy] = 0
                    break
                else:
                    visibility_from_pos[local_x + dx, local_y + dy] = 1
        
        visibility_from_pos[visibility_from_pos == 2] = 0
        return visibility_from_pos

    visibility = np.zeros((width, height), dtype=object)
    # Loop though environment, add each positions visibility map
    for x in range(width):
        for y in range(height):
            if environment[x, y] != TileType.WALL and environment[x, y] != TileType.TABLE:
                visibility[x, y] = calculate_local_visibility(x, y)
    return visibility
