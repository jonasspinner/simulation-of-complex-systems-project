import numpy as np

    
def getDistances(visibilityMatrix : np.ndarray, environment : np.ndarray) -> np.ndarray:
    """
    Parameters
    ----------
    visibilityMatrix
        Holds all visibility maps corresponding to each positions in the environment
    environment
        Used for finding non zero element when initializing distanceMatrix

    Returns
    -------
    distanceMatrix : np.ndarray
        distanceMatrix describes the distance to all states in a radius of 2m 
        (this depends on visibilityMatrix) from a given state.  
    """ 
    
    # Look for a state in environment which is not a wall since those states in visibilityMatrix are empty
    found = False
    while found == False:
        for j in range(5,np.shape(environment)[0]):
            for i in range(5,np.shape(environment)[1]): 
                if environment[j,i] != 0:
                    distanceMatrix = np.full(np.shape(visibilityMatrix[int(j),int(i)]), np.inf, dtype=float)
                    found = True
      
    # Calculate distances from the middle position of the matrix    
    middlePos = [int(np.floor(np.shape(distanceMatrix)[0]/2)), int(np.floor(np.shape(distanceMatrix)[0]/2))]
    iCols = np.linspace(0,np.shape(distanceMatrix)[0]-1,np.shape(distanceMatrix)[0])
    iRows = np.linspace(0,np.shape(distanceMatrix)[1]-1,np.shape(distanceMatrix)[1])
    
    for j in iCols:
        for i in iRows:    
            if int(j) == middlePos[0] and int(i) == middlePos[1]:
                distanceMatrix[int(j),int(i)] = np.inf
            else:
                distanceMatrix[int(j),int(i)] = np.sqrt( (j-middlePos[0])**2 + (i-middlePos[1])**2 )
            
    return distanceMatrix
            
            
def emit(environment : np.ndarray, particleMatrix : np.ndarray, visibilityMatrix : np.ndarray, distanceMatrix : np.ndarray, xPos : int, yPos : int, emissionRate : float)  -> np.ndarray:
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

    Returns
    -------
    particleMatrix : np.ndarray
        particleMatrix describes the amount of particles in every position of the map.
    """           
    
    emission = emissionRate * 1/distanceMatrix
    visibilityMap = visibilityMatrix[xPos,yPos]
    # visibilityMap har 0 for non visible states, i.e no emission. 
    emission = np.where(visibilityMap != 0, emission, 0)
    
    # Condition such that range is not outside of enviromental map (same dimensions as particle matrix) 
    # Look left
    if xPos >= np.ceil(np.shape(emission)[1]/2):
        rangeColMin = int(np.floor(np.shape(visibilityMatrix[xPos,yPos])[1]/2))
    else:
        rangeColMin = int(xPos)
        
    # Look right
    if np.shape(environment)[0]-xPos > np.ceil(np.shape(emission)[0]/2):
        rangeColMax = int(np.floor(np.shape(visibilityMatrix[xPos,yPos])[1]/2))
    else:
        rangeColMax = int(np.shape(environment)[1]-xPos)
        
    # Look up
    if yPos >= np.ceil(np.shape(emission)[1]/2):
        rangeRowMin = int(np.floor(np.shape(visibilityMatrix[xPos,yPos])[0]/2))
    else:
        rangeRowMin = int(yPos)
        
    # Look down
    if np.shape(environment)[1]-yPos > np.ceil(np.shape(emission)[1]/2):
        rangeRowMax = int(np.floor(np.shape(visibilityMatrix[xPos,yPos])[0]/2))
    else:
        rangeRowMax = int(np.floor(np.shape(visibilityMatrix[xPos,yPos])[0]/2))
        
    # Takes care of cases where emission matrix gets outside of particleMatrix
    particleMatrix[(xPos - rangeColMin):(xPos + rangeColMax),(yPos - rangeRowMin):(yPos + rangeRowMax)] = \
        particleMatrix[(xPos - rangeColMin):(xPos + rangeColMax),(yPos - rangeRowMin):(yPos + rangeRowMax)] + \
        emission[(int(np.ceil(np.shape(emission)[0]/2)) - rangeColMin):(int(np.ceil(np.shape(emission)[0]/2)) + rangeColMax), \
                 (int(np.ceil(np.shape(emission)[1]/2)) - rangeRowMin):(int(np.ceil(np.shape(emission)[1]/2)) + rangeRowMax)]
    return particleMatrix
         