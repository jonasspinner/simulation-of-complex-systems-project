import numpy as np 

class Agent:

    def __init__(self,
                pathIn = [],
                pathExit = [],
                state = "OUT",
                eatTime = 300,
                infected = False,
                accDroplets = 0.0):

        self.state = state 
        self.eatTime = eatTime
        self.infected = infected
        self.pathIn = np.asarray(pathIn) #to food + seat
        self.pathExit = np.asarray(pathExit)
        self.accDroplets = accDroplets

        self.position = np.asarray([-1.,-1.])
        self.timeInResturant = 0
        self.stepCounter = 0


    def Step(self):

        if self.state == "GO_IN":
            if len(self.pathIn) > self.stepCounter:
                self.position = self.pathIn[self.stepCounter]
                self.stepCounter += 1
            else:
                self.state = "SITTING"
                self.stepCounter = 0

        elif self.state == "SITTING":
            self.stepCounter += 1

            if self.eatTime < self.stepCounter:
                self.state = "GO_EXIT"
                self.stepCounter = 0

        elif self.state == "GO_EXIT":
            if len(self.pathExit) > self.stepCounter:
                self.position = self.pathExit[self.stepCounter]
                self.stepCounter += 1
            else:
                self.state = "OUT"
                self.stepCounter = 0
        else:
            self.position = [-1,-1]
            self.stepCounter = 0

        self.timeInResturant += 1

        return self.position

    def SetState(self, state):
        self.state = state
    
    def GetState(self):
        return self.state
    
    def GetPathIn(self):
        return self.pathIn

    def AddDroplets(self, droplets):
        self.accDroplets = self.accDroplets + droplets

    def GetPathExit(self):
        return self.pathExit
    
    def GetPosition(self):
        return self.position

    def SetPosition(self, position):
        self.position = self.position


