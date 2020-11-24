from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from agent import Agent, AgentState
from loader import load_environment
from path import find_path, build_graph, building_cmap


def main(save_file_to_disk=False, resolution=1):
    input_map_path = Path(__file__).parent.parent / "data" / "test-map-1.txt"
    output_video_path = Path(__file__).parent.parent / "run-animation.mp4"

    environment, entries, foods, seats = load_environment(str(input_map_path), resolution)
    entry_position = entries[0]
    food_position = foods[0]

    graph = build_graph(environment)

    agents = []
    # Create path to food place from entrance
    path_to_food = find_path(graph, entry_position, food_position)

    # Create agents walk path. This is to avoid calculating the path each iteration.
    for seat_position in seats:
        path_to_seat = find_path(graph, food_position, seat_position)
        path_to_exit = find_path(graph, seat_position, entry_position)
        agents.append(Agent(path_in=path_to_food + path_to_seat, path_out=path_to_exit))

    # Plot code
    fig, ax = plt.subplots(figsize=(5, 3))
    # Plot the map
    height, width = environment.shape
    ax.set(xlim=(0, width), ylim=(0, height))
    ax.imshow(environment, cmap=building_cmap)

    circles = []

    for i, agent in enumerate(agents):
        y, x = agent.position
        circle = plt.Circle((x, y), resolution / 4, fc='k', fill=True)

        circles.append(circle)
        ax.add_patch(circle)

    def update_agents(_frame):
        for agent, circle in zip(agents, circles):
            if agent.state == AgentState.OUTSIDE and np.random.random() < 1 / len(agents):
                agent.state = AgentState.ARRIVING

            agent.step()
            y, x = agent.position
            circle.center = (x, y)
        return circles

    if save_file_to_disk:
        animation = FuncAnimation(fig, update_agents, interval=10, frames=1000, repeat=False)
        animation.save(str(output_video_path), fps=30, extra_args=['-vcodec', 'libx264'], dpi=300)
    else:
        animation = FuncAnimation(fig, update_agents, interval=10)
    plt.show()


if __name__ == '__main__':
    main(save_file_to_disk=True)
