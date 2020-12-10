from typing import Optional, List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

__all__ = ["density_cmap", "building_cmap", "plot_path"]

from loader import Pos

density_cmap = ListedColormap([[0.9, 0.1, 0.1, alpha] for alpha in np.linspace(0, 1, 256)])

building_cmap = ListedColormap([
    [0.4, 0.4, 0.4, 1],  # wall
    [1, 1, 1, 1],  # floor
    [0.9, 0.7, 0.7, 1],  # seat
    [0, 1, 0, 1],  # entry
    [0, 0, 1, 1],  # food
    [1, 0, 1, 1],  # up
    [1, 0, 1, 1],  # right
    [1, 0, 1, 1],  # down
    [1, 0, 1, 1],  # left
    [0.6, 0.6, 0.6, 1],  # table
    [0.9, 0.9, 0.9, 1],  # walking path
])


def plot_path(environment: np.ndarray, path: Optional[List[Pos]] = None) -> None:
    plt.imshow(environment.T, cmap=building_cmap)
    if path is not None:
        xs, ys = zip(*path)
        plt.plot(xs, ys, "k-")
    plt.show()
