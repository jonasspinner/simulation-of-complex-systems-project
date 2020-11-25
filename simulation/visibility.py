import numpy as np

def getVisibilityMaps(environment : np.ndarray, resolution : int)  -> np.ndarray:
    """
    Parameters
    ----------
    environment : matrix
        In correct dimensions, i.e resolution has allready been applied
    resolution : int
        Use this for scale, i.e if we decide that one original square is 50x50 cm,
        then one square in the environment is 50/res x 50/res cm. Need this for 
        the radius of particle emission.

    Returns
    -------
    matrix : np.ndarray
        Matrix with visibility matrices for all possible positions in environment. 
        1 for visible state (i.e a state to which particle emits from a given position)
        0 for non visible states. 
        
        OBS: values of environmental matrix:    
         WALL = 0
         FLOOR = 1
         SEAT = 2
         ENTRY = 3
         FOOD = 4
    """
    
    def getVisibility(environment : np.ndarray, resolution : int, row : int, col : int) -> np.ndarray:        
        # how much is two meters? Assuming 1 (original) square in original map is 50 cm. 
        radius = 4*resolution
        dRadius = np.linspace(0,radius/1.5,10)
        dTheta = np.linspace(0,2*np.pi,10)
        visibilityMap = 2 + np.zeros((radius*2 + 1,radius*2 + 1),dtype=int)
        
        for theta in dTheta:            
            for rad in dRadius:
                
                vRowPos = radius + np.sin(theta)*rad
                vColPos = radius + np.cos(theta)*rad
                
                # Break if outside of map (case if entry/food is on boundry, this way food is enabled to be placed anywhere in the map)
                environmentalRowPos = row + 0.5 + np.sin(theta)*rad              
                if environmentalRowPos > np.shape(environment)[1] or environmentalRowPos < 0:
                    break
                
                environmentalColPos = col + 0.5 + np.cos(theta)*rad         
                if environmentalColPos > np.shape(environment)[0]-1 or environmentalColPos < 0:
                    break
                
                envState = environment[int(np.round(environmentalRowPos)),int(np.round(environmentalColPos))]                  
                if envState in [1,2,3,4]:
                    visibilityMap[int(np.round(vRowPos)),int(np.round(vColPos))] = 1
                if envState == 0:
                    visibilityMap[int(np.round(vRowPos)),int(np.round(vColPos))] = 0
                    break
                
        # Checking for reasonable placement of starting point.
        # visibilityMap[int(np.round(radius)), int(np.round(radius))] = 3   
        
        visibilityMap[visibilityMap==2] = 0
        return visibilityMap
                    
    
    nRow, nCol = np.shape(environment)
    visibilityMatrix = np.zeros((nRow,nCol),dtype=object)
    nRow = np.linspace(0,nRow-1,nRow)
    nCol = np.linspace(0,nCol-1,nCol)
    # Loop though environment, add each positions visibility map
    for i in nRow:
        for j in nCol:
            if environment[int(i),int(j)] != 0:
                visibilityMap = getVisibility(environment, resolution, int(i), int(j))
                visibilityMatrix[int(i),int(j)] = visibilityMap
    return visibilityMatrix
        