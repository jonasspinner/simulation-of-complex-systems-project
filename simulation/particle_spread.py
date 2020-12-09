import numpy as np
from simulation.loader import TileType

class particle_spread:
    def __init__(self,
                 resolution=1,
                 environment = np.zeros((1, 1)),
                 visibilityMatrix = np.zeros((1, 1)),
                 particleMatrix = np.zeros((1, 1)),
                 distanceMatrix = np.zeros((1, 1)),
                 emissionRate = float):
        
        self.resolution = resolution
        self.environment = environment
        self.visibilityMatrix = visibilityMatrix
        self.particleMatrix = particleMatrix
        self.distanceMatrix = distanceMatrix
        self.emissionRate = emissionRate


    def emit(self, posInfectedlist, agent_state, cones)  -> np.ndarray:
        """
        Parameters
        ----------
        environment : matrix
            In correct dimensions, i.e resolution has allready been applied
        particleMatrix : np.ndarray
            particleMatrix describes the amount of particles in every position of the map.
        visibilityMatrix : matrix 3D
            Holds all visibility maps corresponding to each positions in the environment
        distanceMatrix : matrix
            distance to all states in a radius of 2m from current state (same distance matrix for all states)
        posX, posY : int
            The current agents position coordinates
        emissionRate : float
            describes how contaigious the current agent is
            
            
        agent_state : state
            if this is seat, then use cones for vision
        cones : matrix 3D
            contains 4 cone matrices for modifying the vision 
    
        Returns
        -------
        particleMatrix : np.ndarray
            particleMatrix describes the amount of particles in every position of the map.
        """           
        self.particleMatrix = self.particleMatrix*0.9
        
        for pos in posInfectedlist:
            emission = self.emissionRate * 1/self.distanceMatrix
            
            xPos = pos[0]
            yPos = pos[1]
            
            visibilityMap = self.visibilityMatrix[xPos,yPos]
            # visibilityMap has 0 for non visible states, i.e no emission. 
            emission = np.where(visibilityMap != 0, emission, 0)
            
            tile_type = self.environment[xPos, yPos]
            if tile_type == TileType.SEAT:
                if self.environment[xPos + 1, yPos] == TileType.TABLE or self.environment[xPos + 2, yPos] == TileType.TABLE:
                    emission = np.multiply(emission,cones[0,0])
                elif self.environment[xPos, yPos + 1] == TileType.TABLE or self.environment[xPos, yPos + 2] == TileType.TABLE:
                    emission = np.multiply(emission,cones[0,1])
                elif self.environment[xPos - 1, yPos] == TileType.TABLE or self.environment[xPos - 2, yPos] == TileType.TABLE:
                    emission = np.multiply(emission,cones[0,2])
                elif self.environment[xPos, yPos - 1] == TileType.TABLE or self.environment[xPos, yPos - 2] == TileType.TABLE:
                    emission = np.multiply(emission,cones[0,3])
            
            # Condition such that range is not outside of enviromental map (same dimensions as particle matrix) 
            # Look left
            if xPos >= np.ceil(np.shape(emission)[0]/2):
                rangeColMin = int(np.floor(np.shape(self.visibilityMatrix[xPos,yPos])[0]/2))
                
            else:
                rangeColMin = int(xPos)
                
                
            # Look right
            if np.shape(self.environment)[0]-1-xPos >= np.ceil(np.shape(emission)[0]/2):
                rangeColMax = int(np.floor(np.shape(self.visibilityMatrix[xPos,yPos])[0]/2))
            else:
                rangeColMax = int(np.shape(self.environment)[0]-xPos-1)
                
                
            # Look up
            if yPos >= np.ceil(np.shape(emission)[1]/2):
                rangeRowMin = int(np.floor(np.shape(self.visibilityMatrix[xPos,yPos])[1]/2))
            else:
                rangeRowMin = int(yPos)
                
                
            # Look down
            if np.shape(self.environment)[1]-1-yPos >= np.ceil(np.shape(emission)[1]/2):
                rangeRowMax = int(np.floor(np.shape(self.visibilityMatrix[xPos,yPos])[1]/2))
            else:
                rangeRowMax = int(np.shape(self.environment)[1]-yPos-1)
                
                
            # Takes care of cases where emission matrix gets outside of particleMatrix
            self.particleMatrix[(1 + xPos - rangeColMin):(1 + xPos + rangeColMax),(1 + yPos - rangeRowMin):(1 + yPos + rangeRowMax)] = self.particleMatrix[(1 + xPos - rangeColMin):(1 + xPos + rangeColMax),(1 + yPos - rangeRowMin):(1 + yPos + rangeRowMax)] + emission[(int(np.ceil(np.shape(emission)[0]/2)) - rangeColMin):(int(np.ceil(np.shape(emission)[0]/2)) + rangeColMax),(int(np.ceil(np.shape(emission)[1]/2)) - rangeRowMin):(int(np.ceil(np.shape(emission)[1]/2)) + rangeRowMax)]
            self.particleMatrix[self.particleMatrix > 250] = 250
        return self.particleMatrix
    
