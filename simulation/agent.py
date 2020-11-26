from enum import Enum, unique


@unique
class AgentState(Enum):
    OUTSIDE = "OUTSIDE"
    SITTING = "SITTING"
    ARRIVING = "ARRIVING"
    LEAVING = "LEAVING"
    LEFT = "LEFT"


class Agent:
    def __init__(self,
                 path_in=None,
                 path_out=None,
                 state=AgentState.OUTSIDE,
                 time_spent_eating=300,
                 infected=False,
                 accumulated_droplets=0.0):
        if path_in is None:
            path_in = []
        if path_out is None:
            path_out = []
        self.state: AgentState = state
        self.time_spent_eating = time_spent_eating
        self.infected = infected
        self.path_in = path_in  # to food + seat
        self.path_out = path_out
        self.accumulated_droplets = accumulated_droplets
        self.droplets_list = []
        self.position = (-1, -1)
        self.time_spent_in_restaurant = 0
        self.step_counter = 0

    def step(self) -> None:
        if self.state == AgentState.ARRIVING:
            if len(self.path_in) > self.step_counter:
                self.position = self.path_in[self.step_counter]
                self.step_counter += 1
            else:
                self.state = AgentState.SITTING
                self.step_counter = 0

        elif self.state == AgentState.SITTING:
            self.step_counter += 1

            if self.time_spent_eating < self.step_counter:
                self.state = AgentState.LEAVING
                self.step_counter = 0

        elif self.state == AgentState.LEAVING:
            if len(self.path_out) > self.step_counter:
                self.position = self.path_out[self.step_counter]
                self.step_counter += 1
            else:
                self.state = AgentState.LEFT
                self.step_counter = 0
        else:
            self.position = (-1, -1)
            self.step_counter = 0

        self.time_spent_in_restaurant += 1
