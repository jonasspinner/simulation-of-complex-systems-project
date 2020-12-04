from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random

from agent import Agent, AgentState
from emit_particles import getDistances
from loader import load_environment, TileType, select_tiles
from particle_spread import particle_spread
from path import find_path, build_graph, building_cmap
from visibility import getVisibilityMaps
from data_analysis import data_analysis


def main(save_file_to_disk=False, animate = False, do_data_analys = True, resolution=1):

    sitting_min_time = 30*60*resolution
    sitting_max_time = 30*60*resolution

    avarage_time_steps_between_entering = 5*resolution

    chance_of_being_infected = 0.01

    input_map_path = Path(__file__).parent.parent / "data" / "test-map-2.txt"
    output_video_path = Path(__file__).parent.parent / "run-animation.mp4"

    environment = load_environment(str(input_map_path), resolution)
    entries = select_tiles(environment, resolution, TileType.ENTRY)
    foods = select_tiles(environment, resolution, TileType.FOOD)
    seats = select_tiles(environment, resolution, TileType.SEAT)

    entry_position = entries[0]
    food_position = foods[0]

    graph = build_graph(environment)

    agents = []
    accumulated_droplets_list = []
    droplets_list_of_list = []

    risk_density_arriving_list = []
    risk_density_sitting_list = []
    risk_density_leaving_list = []

    time_spent_in_restaurant_list = []

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
    width, height = environment.shape
    ax.set(xlim=(0, width), ylim=(height, 0))
    ax.imshow(environment.T, cmap=building_cmap)

    visibilityMatrix = getVisibilityMaps(environment, resolution)
    distanceMatrix = getDistances(visibilityMatrix, environment)

    particle_map = np.zeros((width, height))
    infection_spread = particle_spread(resolution=1,
                                       environment=environment,
                                       visibilityMatrix=visibilityMatrix,
                                       particleMatrix=particle_map,
                                       distanceMatrix=distanceMatrix,
                                       emissionRate=2.5)

    particle_overlay = ax.imshow(particle_map.T, alpha=0.5, cmap='Reds', vmin=0.0, vmax=25.0)

    circles = []

    for i, agent in enumerate(agents):
        circle = plt.Circle(agent.position, resolution / 4, fc='k', ec='g', fill=True)

        circles.append(circle)
        ax.add_patch(circle)

    def update_agents(_frame):

        print(_frame)

        particle_map = infection_spread.particleMatrix

        infected_pos_list = []

        for agent, circle in zip(agents, circles):
            if agent.state == AgentState.OUTSIDE and np.random.random() < avarage_time_steps_between_entering / len(agents):
                agent.state = AgentState.ARRIVING
                agent.time_spent_eating = random.randint(sitting_min_time, sitting_max_time)
                
                if np.random.random() < chance_of_being_infected:
                    agent.infected = True
                    circle.set_ec('r')

            if agent.state != AgentState.OUTSIDE:

                agent.step()
                circle.center = agent.position

                if agent.state == AgentState.LEFT:

                    accumulated_droplets_list.append(agent.accumulated_droplets)
                    agent.accumulated_droplets = 0

                    droplets_list_of_list.append(agent.droplets_list)
                    risk_density_arriving_list.append(agent.risk_density_arriving)
                    risk_density_sitting_list.append(agent.risk_density_sitting)
                    risk_density_leaving_list.append(agent.risk_density_leaving)

                    agent.droplets_list = []

                    time_spent_in_restaurant_list.append(agent.time_spent_in_restaurant)
                    agent.time_spent_in_restaurant = 0

                    if agent.infected:
                        agent.infected = False
                        circle.set_ec('g')

                    agent.state = AgentState.OUTSIDE

                else:
                    if agent.infected:
                        infected_pos_list.append(agent.position)
                    else:
                        # agent.accumulated_droplets += particle_map[agent.position]
                        # agent.droplets_list.append(particle_map[agent.position])
                        agent.accumulated_droplets += particle_map[agent.position[0], agent.position[1]]
                        agent.droplets_list.append(particle_map[agent.position[0], agent.position[1]])

                        agent.add_risk_density(particle_map[agent.position[0], agent.position[1]])

        # infection_spread = GaussianSpread(infectionMap=particle_map, resolution=resolution)
        particle_map = infection_spread.emit(infected_pos_list)
        particle_overlay.set_data(particle_map.T)

        return circles, particle_overlay

    if not animate:
        for i in range(40000):
            update_agents(i)

    elif save_file_to_disk:
        animation = FuncAnimation(fig, update_agents, interval=1, frames=2500, repeat=False)
        animation.save(str(output_video_path), fps=30, extra_args=['-vcodec', 'libx264'], dpi=300)
    else:
        animation = FuncAnimation(fig, update_agents, interval=10)
        plt.show()
    
    plt.close()

    if do_data_analys:
        data_analysis(accumulated_droplets_list, droplets_list_of_list, risk_density_arriving_list, risk_density_sitting_list, risk_density_leaving_list)

if __name__ == '__main__':
    main(save_file_to_disk=True)
