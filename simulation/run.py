import random
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from simulation.agent import Agent, AgentState
from simulation.data_analysis import data_analysis, sum_of_list_in_list
from simulation.emit_particles import getDistances, getDirectedSpread
from simulation.loader import load_environment, TileType, select_tiles
from simulation.particle_spread import particle_spread
from simulation.path import find_path, build_graph
from simulation.visibility import getVisibilityMaps
from simulation.visualizations import building_cmap, density_cmap


def main(do_data_analysis=False, resolution=3):
    setting = 5
    # 1 = Do animation and plot live
    # 2 = Do animation and save to file (no live plot)
    # 3 = Do one run without animation
    # 4 = Do multiple run with different infection rates
    # 5 = Do multiple run with different max amount of people

    max_ratio_agents = 1  # 1=100%, 0.5=50%
    iterations_multiple_run = 10000

    sitting_min_time = 15 * 60 * resolution
    sitting_max_time = 45 * 60 * resolution

    avarage_time_steps_between_entering = 1 / (1 * resolution)

    chance_of_being_infected = 0.01

    input_map_path = Path(__file__).parent.parent / "data" / "chalmers_karresturang_normal.txt"
    output_video_path = Path(__file__).parent.parent / "run-animation.mp4"

    environment = load_environment(str(input_map_path), resolution)
    entries = select_tiles(environment, resolution, TileType.ENTRY)
    foods = select_tiles(environment, resolution, TileType.FOOD)
    seats = select_tiles(environment, resolution, TileType.SEAT)

    entry_position = entries[0]
    food_position = foods[0]

    graph = build_graph(environment)

    agents = []
    accumulated_risk_list = []
    risk_list_of_list = []

    risk_density_arriving_list = []
    risk_density_sitting_list = []
    risk_density_leaving_list = []

    time_spent_in_restaurant_list = []

    # Create agents walk path. This is to avoid calculating the path each iteration.
    for seat_position in seats:
        path_to_food = find_path(graph, entry_position, food_position)
        path_to_seat = find_path(graph, food_position, seat_position)
        path_to_exit = find_path(graph, seat_position, entry_position)
        agents.append(Agent(path_in=path_to_food + path_to_seat, path_out=path_to_exit))

    total_number_of_seats = len(agents)

    max_number_agents = int(max_ratio_agents * total_number_of_seats)

    # Plot code
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    # Plot the map
    width, height = environment.shape
    ax1.set(xlim=(-1, width), ylim=(height, -1))
    ax1.axis('off')
    ax1.imshow(environment.T, cmap=building_cmap)

    visibility_map_path = input_map_path.with_suffix(".visibility.npy")
    if visibility_map_path.exists():
        visibilityMatrix = np.load(visibility_map_path, allow_pickle=True)
    else:
        visibilityMatrix = getVisibilityMaps(environment, resolution, screen=False)
        np.save(visibility_map_path, visibilityMatrix)
    distanceMatrix = getDistances(visibilityMatrix, environment, resolution)
    cones = getDirectedSpread(visibilityMatrix, environment, resolution)

    particle_map = np.zeros((width, height))
    infection_spread = particle_spread(resolution=resolution,
                                       environment=environment,
                                       visibilityMatrix=visibilityMatrix,
                                       particleMatrix=particle_map,
                                       distanceMatrix=distanceMatrix,
                                       emissionRate=3)

    particle_overlay = ax1.imshow(particle_map.T, alpha=0.5, cmap=density_cmap, vmin=0.0, vmax=25.0)

    plot_risk_density, = ax2.plot([], [], color="blue")
    ax2.set_xlabel("Timestep for agent")
    ax2.set_ylabel("Local risk density (blue)")
    ax3 = ax2.twinx()
    plot_risk_density_acc, = ax3.plot([], [], color="green")
    ax3.set_ylabel("Accumulated risk density (green)")

    fig.tight_layout()

    circles = []

    for i, agent in enumerate(agents):
        circle = plt.Circle(agent.position, resolution / 4, fc='k', ec='g', fill=True)

        circles.append(circle)
        ax1.add_patch(circle)

    def update_agents(_frame):
        # print(_frame)

        particle_map = infection_spread.particleMatrix

        current_number_agents_in_resturant = 0
        for agent in agents:
            if agent.state != AgentState.OUTSIDE:
                current_number_agents_in_resturant += 1

        infected_pos_list = []

        for agent, circle in zip(agents, circles):
            if agent.state == AgentState.OUTSIDE and np.random.random() < avarage_time_steps_between_entering / len(
                    agents):
                if current_number_agents_in_resturant <= max_number_agents:

                    agent.state = AgentState.ARRIVING
                    agent.time_spent_eating = random.randint(sitting_min_time, sitting_max_time)

                    if agents.index(agent) == 0:
                        circle.set_ec('b')
                        circle.set_fc('b')

                    if np.random.random() < chance_of_being_infected:
                        agent.infected = True
                        circle.set_ec('r')
                        circle.set_fc('k')

            if agent.state != AgentState.OUTSIDE:

                agent.step()
                circle.center = agent.position

                if agent.state == AgentState.LEFT:

                    accumulated_risk_list.append(agent.accumulated_risk)
                    agent.accumulated_risk = 0

                    risk_list_of_list.append(agent.risk_density_complete)
                    risk_density_arriving_list.append(agent.risk_density_arriving)
                    risk_density_sitting_list.append(agent.risk_density_sitting)
                    risk_density_leaving_list.append(agent.risk_density_leaving)

                    agent.risk_density_complete = []

                    agent.accumulated_risk_list = []

                    agent.risk_density_arriving = []
                    agent.risk_density_sitting = []
                    agent.risk_density_leaving = []

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

                        agent.add_risk_density(particle_map[agent.position[0], agent.position[1]])

                        if agents.index(agent) == 0:
                            risk_density = agent.risk_density_arriving + agent.risk_density_sitting + agent.risk_density_leaving
                            plot_risk_density.set_data(range(len(risk_density)), risk_density)
                            ax2.set(xlim=(0, len(risk_density)), ylim=(-1, max(risk_density) + 1))

                            plot_risk_density_acc.set_data(range(len(agent.accumulated_risk_list)),
                                                           agent.accumulated_risk_list)
                            ax3.set_ylim([-1, max(agent.accumulated_risk_list) + 1])

        # infection_spread = GaussianSpread(infectionMap=particle_map, resolution=resolution)
        particle_map = infection_spread.emit(infected_pos_list, agent.state, cones)
        particle_overlay.set_data(particle_map.T)

        return circles, particle_overlay, ax2, ax3

    if setting == 1:
        animation = FuncAnimation(fig, update_agents, interval=10)
        plt.show()

    elif setting == 2:
        animation = FuncAnimation(fig, update_agents, interval=1, frames=500, repeat=False)
        animation.save(str(output_video_path), fps=30, extra_args=['-vcodec', 'libx264'], dpi=300)

    elif setting == 3:
        for i in range(10000):
            update_agents(i)

    elif setting == 4:
        chance_of_being_infected = 0.00
        print("# chance_of_being_infected; ",  "median risk density arriving; ",
              "median risk density sitting; ", "median risk density leaving ", "mean risk density arriving; ",
              "mean risk density arriving; ", "mean risk density leaving")
        for p in range(20):

            chance_of_being_infected += 0.01

            accumulated_risk_list = []
            risk_list_of_list = []
            risk_density_arriving_list = []
            risk_density_sitting_list = []
            risk_density_leaving_list = []

            risk_density_arriving_list_sum = []
            risk_density_sitting_list_sum = []
            risk_density_leaving_list_sum = []

            for agent in agents:
                agent.reset()

            for i in range(iterations_multiple_run):
                update_agents(i)

            risk_density_arriving_list_sum = sum_of_list_in_list(risk_density_arriving_list.copy())
            risk_density_sitting_list_sum = sum_of_list_in_list(risk_density_sitting_list.copy())
            risk_density_leaving_list_sum = sum_of_list_in_list(risk_density_leaving_list.copy())

            print(round(chance_of_being_infected, 2), ";", round(statistics.median(risk_density_arriving_list_sum), 2),
                  ";", round(statistics.median(risk_density_sitting_list_sum), 2), ";",
                  round(statistics.median(risk_density_leaving_list_sum), 2), ";",
                  round(statistics.mean(risk_density_arriving_list_sum), 2), ";",
                  round(statistics.mean(risk_density_sitting_list_sum), 2), ";",
                  round(statistics.mean(risk_density_leaving_list_sum), 2))

    elif setting == 5:
        max_number_agents = 50
        print("# iterations_multiple_run:", iterations_multiple_run, "  chance_of_being_infected:", 
                chance_of_being_infected, "  resolution:", resolution)

        print("# max_number_agents; ", "total number of seats; ", "median risk density arriving; ",
              "median risk density sitting; ", "median risk density leaving ", "mean risk density arriving; ",
              "mean risk density arriving; ", "mean risk density leaving")
        while max_number_agents <= total_number_of_seats:

            accumulated_risk_list = []
            risk_list_of_list = []
            risk_density_arriving_list = []
            risk_density_sitting_list = []
            risk_density_leaving_list = []

            risk_density_arriving_list_sum = []
            risk_density_sitting_list_sum = []
            risk_density_leaving_list_sum = []

            for agent in agents:
                agent.reset()

            for i in range(iterations_multiple_run):
                update_agents(i)

            risk_density_arriving_list_sum = sum_of_list_in_list(risk_density_arriving_list.copy())
            risk_density_sitting_list_sum = sum_of_list_in_list(risk_density_sitting_list.copy())
            risk_density_leaving_list_sum = sum_of_list_in_list(risk_density_leaving_list.copy())

            print(round(max_number_agents, 2), ";", round(total_number_of_seats, 2), ";",
                  round(statistics.median(risk_density_arriving_list_sum), 2), ";",
                  round(statistics.median(risk_density_sitting_list_sum), 2), ";",
                  round(statistics.median(risk_density_leaving_list_sum), 2), ";",
                  round(statistics.mean(risk_density_arriving_list_sum), 2), ";",
                  round(statistics.mean(risk_density_sitting_list_sum), 2), ";",
                  round(statistics.mean(risk_density_leaving_list_sum), 2))

            max_number_agents += 50

    plt.close()

    if do_data_analysis:
        data_analysis(accumulated_risk_list, risk_list_of_list, risk_density_arriving_list, risk_density_sitting_list,
                      risk_density_leaving_list)


if __name__ == '__main__':
    main()
