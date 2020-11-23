from itertools import product
from typing import Optional, List

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

from simulation.loader import TileType, Pos

building_cmap = ListedColormap([
    [0.5, 0.5, 0.5, 1],  # wall
    [1, 1, 1, 1],  # floor
    [1, 0, 0, 1],  # seat
    [0, 1, 0, 1],  # entry
    [0, 0, 1, 1]  # food
])


def distance(u: Pos, v: Pos) -> float:
    return np.linalg.norm(np.array(u) - np.array(v))


def build_graph(environment: np.ndarray) -> nx.DiGraph:
    height, width = environment.shape
    positions = list(product(range(height), range(width)))

    graph = nx.DiGraph()
    graph.add_nodes_from(positions)

    def neighbors(pos: Pos) -> List[Pos]:
        i, j = pos
        candidates = [(i + di, j + dj) for di, dj
                      in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]]
        return [(i, j) for i, j in candidates
                if 0 <= i < height and 0 <= j < width and environment[i, j] != TileType.WALL]

    for u in positions:
        if environment[u] == TileType.WALL:
            continue
        for v in neighbors(u):
            non_floor_movement = environment[u] != TileType.FLOOR or environment[v] != TileType.FLOOR
            cost = distance(u, v)
            if non_floor_movement:
                cost += 10.0
            graph.add_edge(u, v, cost=cost)
    return graph


def find_path(graph: nx.Graph, start: Pos, end: Pos) -> List[Pos]:
    # noinspection PyTypeChecker
    return nx.astar_path(graph, start, end, heuristic=distance, weight="cost")


def plot_path(environment: np.ndarray, path: Optional[List[Pos]] = None) -> None:
    plt.imshow(environment, cmap=building_cmap)
    if path is not None:
        ys, xs = zip(*path)
        plt.plot(xs, ys, "k-")
    plt.show()
