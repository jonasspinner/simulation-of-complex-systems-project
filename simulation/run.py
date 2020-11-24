from path import find_path, plot_path, build_graph
from loader import load_environment
from agent import Agent
import matplotlib.pyplot as plot 
import numpy as np 
import networkx as nx

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

building_cmap = ListedColormap([
    [0.5, 0.5, 0.5, 1],  # wall
    [1, 1, 1, 1],  # floor
    [1, 0, 0, 1],  # seat
    [0, 1, 0, 1],  # entry
    [0, 0, 1, 1]  # food
])

runSaveFile = False
res = 1
environment, entryPosition, foodPosition, seatPositions = load_environment("map1", res)

environmentGraph = build_graph(environment)

agentPop = []
#Create path to food place from entrence
pathToFood = find_path(environmentGraph, entryPosition[0], foodPosition[0])

#Create agents walk path. This is to avoide calculating the path each iteration.
for x in seatPositions:
    pathToSeat = find_path(environmentGraph, foodPosition[0], x)
    pathExit = find_path(environmentGraph, x, entryPosition[0])
    agentPop.append( Agent(pathIn = pathToFood+pathToSeat, pathExit = pathExit))


#Plot code
fig, ax1 = plt.subplots(figsize=(5, 3))
#Plot the map
height, width = environment.shape
ax1.set(xlim=(0, width), ylim=(0, height))
im = plt.imshow(environment, cmap=building_cmap)

circleList = []

for agent in range(len(agentPop)):
    tmpPosition = agentPop[agent].GetPosition()
    circle = plt.Circle((tmpPosition[0], tmpPosition[1]), res/4, fc='k', fill=True)

    circleList.append(circle)
    ax1.add_patch(circleList[agent])


def updateAgents(frame):

    for agent in range(len(agentPop)):
        if agentPop[agent].GetState() == "OUT" and np.random.random() < 1/len(agentPop):
            agentPop[agent].SetState("GO_IN")

        tmpPosition=agentPop[agent].Step()

        circleList[agent].center = (tmpPosition[1],tmpPosition[0])

    return circleList

if runSaveFile:
    animation = FuncAnimation(fig, updateAgents, interval=10, frames=1000, repeat=False)
    animation.save('runAnimiation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
else:
    animation = FuncAnimation(fig, updateAgents, interval=10)
plt.show()