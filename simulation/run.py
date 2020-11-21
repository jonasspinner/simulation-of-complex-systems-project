from path import find_path, plot_path
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

res = 1
environment, entryPosition, foodPosition, seatPositions = load_environment("map1", res)

agentPop = []
#Create path to food place from entrence
pathToFood = find_path(environment, entryPosition[0], foodPosition[0])

#Create agents walk path. This is to avoide calculating the path each iteration.
for x in seatPositions:
    pathToSeat = find_path(environment, foodPosition[0], x)
    pathExit = find_path(environment, x, entryPosition[0])
    agentPop.append( Agent(pathIn = pathToFood+pathToSeat, pathExit = pathExit))

run = True
while run:
    pos = agentPop[0].Step()
    if pos != (-1,-1):
        a = 1
    else:
        run = False


#Plot code
fig, ax = plt.subplots(figsize=(5, 3))
#Plot the map
height, width = environment.shape
ax.set(xlim=(0, width), ylim=(0, height))
im = plt.imshow(environment, cmap=building_cmap)
#Plot walk pattern
path = agentPop[0].GetPathIn()
ys, xs = zip(*path)
line, = ax.plot(xs, ys, "k-")


def updateAgents(frame):

    #Get paths from agents
    pathEnter = agentPop[frame].GetPathIn()
    pathExit = agentPop[frame].GetPathExit()
    pathTotal = pathEnter + pathExit

    #Get it in nice format
    ys, xs = zip(*pathTotal)

    #Update the line
    line.set_xdata(xs)
    line.set_ydata(ys)

    return line


animation = FuncAnimation(fig, updateAgents, frames = len(agentPop), interval=100, repeat=True)

plt.show()