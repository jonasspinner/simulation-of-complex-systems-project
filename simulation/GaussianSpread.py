from scipy.ndimage import gaussian_filter
import numpy as np

class GaussianSpread:
    def __init__(self,
                 infectionMap = np.zeros((1, 1)),
                 resolution=1):
        self.infectionMap = infectionMap
        self.resolution = resolution


    def Step(self, posInfectedlist):
        self.infectionMap = self.infectionMap*0.99
        for infected in posInfectedlist:
            self.infectionMap[infected[0]][infected[1]]=self.infectionMap[infected[0]][infected[1]]+50*self.resolution
        self.infectionMap = gaussian_filter(self.infectionMap, sigma=0.5)

        return self.infectionMap