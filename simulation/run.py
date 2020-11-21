from path import find_path_networkx, plot_path
from mapLayout import load_environment
import matplotlib.pyplot as plot 
import numpy as np 

environment = load_environment("map1", 1)

plot.matshow(environment) 
plot.show() 

path = find_path_networkx(environment, [54,15], [50,25])
#plot_path(environment, path)