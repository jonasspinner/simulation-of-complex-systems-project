import numpy as np

    
def getDistances(visibilityMatrix : np.ndarray) -> np.ndarray:
    """
    Parameters
    ----------
        Holds all visibility maps corresponding to each positions in the environment

    Returns
    -------
    distanceMatrix : np.ndarray
        distanceMatrix describes the distance to all states in a radius of 2m 
        (this depends on visibilityMatrix) from a given state.  
    """
    
    #TODO: maybe collect all distanceMatrices in a large 3D matrix as in case with visibilies. 
    
    distanceMatrix = np.inf + np.zeros(np.shape(visibilityMatrix[0,0]),dtype=float)
    middlePos = [np.ceil(np.shape(distanceMatrix)[0]/2),np.ceil(np.shape(distanceMatrix)[0]/2)]
    
    for i in np.shape(distanceMatrix)[0]:
        if i == middlePos[0]:
            continue    
        for j in np.shape(distanceMatrix)[1]:    
            if j == middlePos[1] :
                continue
            distanceMatrix[i,j] = np.sqrt( (i-middlePos[0])**2 + (j-middlePos[1])**2 )
            
    return distanceMatrix
            
            
def emit(environment : np.ndarray, particleMatrix : np.ndarray, visibilityMatrix : np.ndarray, xPos : int, yPos : int, emissionRate : float)  -> np.ndarray:
    """
    Parameters
    ----------
    environment : matrix
        In correct dimensions, i.e resolution has allready been applied
    particleMatrix : np.ndarray
        particleMatrix describes the amount of particles in every position of the map.
    visibilityMatrix : matrix 3D
        Holds all visibility maps corresponding to each positions in the environment
    posX, posY : int
        The current agents position coordinates
    emissionRate : float
        describes how contaigious the current agent is

    Returns
    -------
    particleMatrix : np.ndarray
        particleMatrix describes the amount of particles in every position of the map.
    """           
    
    emission = emissionRate * 1/getDistances(visibilityMatrix)
    
    rangeMin = int(np.floor(np.shape(visibilityMatrix[xPos,yPos])[0]/2))
    rangeMax = int(np.ceil(np.shape(visibilityMatrix[xPos,yPos])[0]/2))
    
    particleMatrix[(xPos - rangeMin):(xPos + rangeMax),(yPos - rangeMin):(yPos + rangeMax)] = particleMatrix[(xPos - rangeMin):(xPos + rangeMax),(yPos - rangeMin):(yPos + rangeMax)] + emission
    return particleMatrix
    
def evaporation(particleMatrix : np.ndarray, evaporationMatrix : np.ndarray)  -> np.ndarray:
    """
    Parameters
    ----------
    particleMatrix : np.ndarray
        particleMatrix describes the amount of particles in every position of the map.
    evaporationMatrix : np.ndarray
        Enables having different evaporation rates at different parts of the map. Could 
        modek air ventilation. All elements could also just be the same.
        Values is \in [0,1].

    Returns
    -------
    particleMatrix : np.ndarray
        particleMatrix describes the amount of particles in every position of the map.
        This is after evaporation and should be done in the end of each timestep.
    """   
    return particleMatrix*evaporationMatrix        