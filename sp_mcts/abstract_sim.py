import numpy as np

class AbstractSimulator:
    def __init__(self, agents: list, goals:list, grid_dim:tuple, shelfs:list, req_shelfs:list):
        self.agents = agents
        self.goals = goals
        self.grid_dim = grid_dim
        self.shelfs = shelfs
        self.state = sim_state()

    def reset(self, state: np.array):

