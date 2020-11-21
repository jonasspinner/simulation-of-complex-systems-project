class Agent:

    def __init__(self,
                pathIn = [],
                pathExit = [],
                state = 0,
                eatTime = 30,
                infected = False,
                accDroplets = 0):

        self.state = state 
        self.infected = infected
        self.pathIn = pathIn #to food + seat
        self.pathExit = pathExit
        self.accDroplets = accDroplets
        self.timeInResturant = 0
        self.stepCounter = 0
        Status = int
        self.OUT:  Status = 0
        self.GO_IN: Status = 1
        self.SITTING: Status = 3
        self.GO_EXIT:  Status = 4

    def Step(self):
        currentPos = (-1,-1)
        
        if self.state == self.GO_IN:
            if len(self.pathIn) > self.stepCounter:
                currentPos = self.pathIn[self.stepCounter]
                self.stepCounter += 1
            else:
                self.state = self.SITTING
                self.stepCounter = 0

        elif self.state == self.SITTING:
            currentPos = self.pathIn[len(self.pathIn)-1]
            self.stepCounter += 1

        elif self.state == self.GO_EXIT:
            if len(self.stepCounter) > self.stepCounter:
                currentPos = self.pathIn[self.stepCounter]
                self.stepCounter += 1
            else:
                self.state = self.OUT
                self.stepCounter = 0

        self.timeInResturant += 1

        return currentPos

    def SetState(self, state):
        self.state = state
    
    def GetState(self):
        return self.state
    
    def GetPathIn(self):
        return self.pathIn

    def GetPathExit(self):
        return self.pathExit
    
    def SetPosition(self, position):
        self.position = position
