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
    [0, 0, 1, 1],  # food
    [1, 0, 1, 1],  # up
    [1, 0, 1, 1],  # right
    [1, 0, 1, 1],  # down
    [1, 0, 1, 1]  # left
])


def distance(u: Pos, v: Pos) -> float:
    return np.linalg.norm(np.array(u) - np.array(v))


def build_graph(environment: np.ndarray) -> nx.DiGraph:
    height, width = environment.shape
    positions = list(product(range(height), range(width)))

    graph = nx.DiGraph()
    graph.add_nodes_from(positions)

    def tiles_from_deltas(pos: Pos, deltas: List[Pos]) -> List[Pos]:
        i, j = pos
        candidates = [(i + di, j + dj) for di, dj in deltas]
        return [(i, j) for i, j in candidates
                if 0 <= i < height and 0 <= j < width and environment[i, j] != TileType.WALL]

    def neighbors(pos: Pos) -> List[Pos]:
        return tiles_from_deltas(pos, [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)])

    direction_deltas = {
        TileType.ONEWAY_UP: [(-1, -1), (-1, 0), (-1, 1)],
        TileType.ONEWAY_RIGHT: [(-1, 1), (0, 1), (1, 1)],
        TileType.ONEWAY_DOWN: [(1, 1), (1, 0), (1, -1)],
        TileType.ONEWAY_LEFT: [(-1, -1), (1, -1), (0, -1)]
    }

    for u in positions:
        if environment[u] == TileType.WALL:
            continue

        target_tiles = neighbors(u)\
            if environment[u] not in direction_deltas\
            else tiles_from_deltas(u, direction_deltas[environment[u]])

        for v in target_tiles:
            seat_movement = environment[u] == TileType.SEAT or environment[v] == TileType.SEAT
            cost = distance(u, v)
            if seat_movement:
                cost += 10.0
            graph.add_edge(u, v, cost=cost)
    return graph


def find_path(graph: nx.DiGraph, start: Pos, end: Pos) -> List[Pos]:
    # noinspection PyTypeChecker
    return nx.astar_path(graph, start, end, heuristic=distance, weight="cost")


def plot_path(environment: np.ndarray, path: Optional[List[Pos]] = None) -> None:
    plt.imshow(environment, cmap=building_cmap)
    if path is not None:
        ys, xs = zip(*path)
        plt.plot(xs, ys, "k-")
    plt.show()
