from itertools import product
from typing import List, Mapping, Any

import networkx as nx
import numpy as np

from simulation.loader import TileType, Pos

__all__ = ["distance", "build_graph", "find_path"]


def distance(u: Pos, v: Pos) -> float:
    return np.linalg.norm(np.array(u) - np.array(v))


def build_graph(environment: np.ndarray) -> nx.DiGraph:
    width, height = environment.shape
    positions = list(product(range(width), range(height)))

    graph = nx.DiGraph()
    graph.add_nodes_from(positions)

    non_passable = {TileType.WALL, TileType.TABLE}

    def tiles_from_deltas(pos: Pos, deltas: List[Pos]) -> List[Pos]:
        x, y = pos
        candidates = [(x + dx, y + dy) for dx, dy in deltas]
        return [(x, y) for x, y in candidates
                if 0 <= x < width and 0 <= y < height and environment[x, y] not in non_passable]

    def neighbors(pos: Pos) -> List[Pos]:
        return tiles_from_deltas(pos, [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)])

    direction_deltas: Mapping[TileType, List[Pos]] = {
        TileType.ONEWAY_UP: [(-1, -1), (0, -1), (1, -1)],  # dy = -1
        TileType.ONEWAY_RIGHT: [(1, -1), (1, 0), (1, 1)],  # dx = 1
        TileType.ONEWAY_DOWN: [(-1, 1), (0, 1), (1, 1)],  # dy = 1
        TileType.ONEWAY_LEFT: [(-1, -1), (-1, 0), (-1, 1)]  # dx = -1
    }

    def cost(u: Pos, v: Pos) -> float:
        value = distance(u, v)
        if environment[u] == TileType.WALL or environment[v] == TileType.WALL:
            value = np.inf
        if environment[v] == TileType.SEAT:
            value *= 2.0
        if environment[u] == TileType.WALKING_PATH and environment[v] == TileType.WALKING_PATH:
            value *= 0.5
        return value

    for u in positions:
        if environment[u] == TileType.WALL:
            continue

        target_tiles = neighbors(u) \
            if environment[u] not in direction_deltas \
            else tiles_from_deltas(u, direction_deltas[environment[u]])

        for v in target_tiles:
            graph.add_edge(u, v, cost=cost(u, v))
    return graph


def find_path(graph: nx.DiGraph, start: Pos, end: Pos, random_deviation: float = 0.6) -> List[Pos]:
    """

    Parameters
    ----------
    graph : nx.DiGraph
    start : Pos
    end : Pos
    random_deviation : float
        If non-zero, draw values from a normal distribution for each position. The absolute difference between the
        values are factored into the edge cost. This results in more random looking graphs.
    """
    node_values = {u: np.random.uniform(low=0, high=random_deviation) for u in graph.nodes}

    def cost_with_deviation(u: Pos, v: Pos, d: Mapping[Any, Any]) -> float:
        return d["cost"] * (1 + np.abs(node_values[u] - node_values[v]))

    # noinspection PyTypeChecker
    return nx.astar_path(graph, start, end, heuristic=distance, weight=cost_with_deviation)
