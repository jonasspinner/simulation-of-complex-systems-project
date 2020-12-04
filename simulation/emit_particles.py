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
                    distanceMatrix = np.full(np.shape(visibilityMatrix[int(j),int(i)]), 1, dtype=float)
                    found = True
      
    # Calculate distances from the middle position of the matrix    
    middlePos = [int(np.floor(np.shape(distanceMatrix)[0]/2)), int(np.floor(np.shape(distanceMatrix)[0]/2))]
    iCols = np.linspace(0,np.shape(distanceMatrix)[0]-1,np.shape(distanceMatrix)[0])
    iRows = np.linspace(0,np.shape(distanceMatrix)[1]-1,np.shape(distanceMatrix)[1])
    
    for j in iCols:
        for i in iRows:    
            if int(j) == middlePos[0] and int(i) == middlePos[1]:
                distanceMatrix[int(j),int(i)] = 0.5
            else:
                distanceMatrix[int(j),int(i)] = np.sqrt( (j-middlePos[0])**2 + (i-middlePos[1])**2 )
            
    return distanceMatrix
         