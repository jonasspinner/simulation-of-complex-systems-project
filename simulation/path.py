from itertools import product
import numpy as np
import networkx as nx
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from typing import Tuple, Optional, List, TypeVar

Tile = int
Pos = Tuple[int, int]
T = TypeVar("T")

WALL:  Tile = 0
FLOOR: Tile = 1
SEAT:  Tile = 2
ENTRY: Tile = 3
FOOD:  Tile = 4

building_cmap = ListedColormap([
    [0.5, 0.5, 0.5, 1],  # wall
    [1, 1, 1, 1],  # floor
    [1, 0, 0, 1],  # seat
    [0, 1, 0, 1],  # entry
    [0, 0, 1, 1]   # food
])


def load_environment() -> np.ndarray:
    return np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 0, 2, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 0, 2, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0],
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 0, 2, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 0, 2, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

#plt.imshow(load_environment(), cmap=building_cmap)
#plt.show()

def find_path_pathlib(environment: np.ndarray, start: Pos, end: Pos) -> List[Pos]:
    # `grid` could be reused.
    # The values of the matrix signify the walking cost and a cost of zero signifies unpassable tiles.
    # Giving seats, entries and food a higher cost prevents agents from walking over seats.
    matrix = np.ones_like(environment)
    matrix[environment == WALL]  = 0
    matrix[environment == SEAT]  = 10
    matrix[environment == ENTRY] = 10
    matrix[environment == FOOD]  = 10
    grid = Grid(matrix=matrix.T)  # The coordinates for the numpy array and pathfinding are flipped.

    start = grid.node(*start)
    end = grid.node(*end)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    return path

def distance(u: Pos, v: Pos) -> float:
    return np.linalg.norm(np.array(u) - np.array(v))

def build_graph(environment: np.ndarray) -> nx.DiGraph:

    Tile = int

    WALL:  Tile = 0
    FLOOR: Tile = 1
    SEAT:  Tile = 2
    ENTRY: Tile = 3
    FOOD:  Tile = 4

    width, height = environment.shape
    positions = list(product(range(width), range(height)))

    graph = nx.DiGraph()
    graph.add_nodes_from(positions)

    for u in positions:
        for v in positions:
            d = distance(u, v)
            if d <= 1.5 and u != v and environment[u] != WALL and environment[v] != WALL:
                if environment[u] != FLOOR or environment[v] != FLOOR:
                    d += 10
                graph.add_edge(u, v, distance=d)

    return graph

def find_path_networkx(environment: nx.networkx, start: Pos, end: Pos) -> List[Pos]:
    print("-----")
    graph = build_graph(environment)
    print("-----")
    # noinspection PyTypeChecker
    return nx.astar_path(graph, start, end, heuristic=distance, weight="distance")

def plot_path(environment: np.ndarray, path: Optional[List[Pos]] = None) -> None:
    plt.imshow(environment, cmap=building_cmap)
    if path is not None:
        ys, xs = zip(*path)
        plt.plot(xs, ys, "k-")
    plt.show()

def choose(options: List[T]) -> T:
    return options[np.random.randint(len(options))]

def select_tiles(environment: np.ndarray, tile_type: Tile) -> List[Tile]:
    # noinspection PyTypeChecker
    return list(zip(*np.where(environment == tile_type)))

def simulate_agent() -> None:
    environment = load_environment()

    entries = select_tiles(environment, ENTRY)
    seats   = select_tiles(environment, SEAT)
    foods   = select_tiles(environment, FOOD)

    # A random choice of waypoints.
    waypoints = [choose(entries), seat := choose(seats), choose(foods), seat, choose(entries)]

    for i in range(len(waypoints) - 1):
        path = find_path_networkx(environment, waypoints[i], waypoints[i+1])
        plot_path(environment, path)

#simulate_agent()