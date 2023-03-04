import numpy as np
from enum import Enum

from config import n_agents, n_requests, default_layout, verbose, goal_coords, shelf_coords, Actions
# from config import verbose

class AbstractSimulator:
    def __init__(self, obs, goals:list, shelfs:list, req_shelfs:list):
        '''
        Initializes the abstract simulator
        
        Parameters
        ----------
        obs : observation
            The observations of the simulation
        goals : list of goals
            The goals of the simulation (coords)
        shelfs : list of shelves
            The shelves of the simulation (coords)
        req_shelfs : list of shelf requests
            The shelf requests of the simulation
        '''
        self.obs = obs
        self.goals = goals
        self.shelfs = shelfs
        self.req_shelfs = req_shelfs
        self.state = self.init_vector_state()

    def init_vector_state(self, verbose=verbose) -> np.array:
        '''
        Returns the current state of the simulation as a vector
        '''

        state = np.array([])

        for i in range(len(self.obs)):
            agent_properties = np.array([i])
            for j in range(3):
                agent_properties = np.append(agent_properties, self.obs[i][j])
            state = np.append(state, agent_properties)  

        for i in range(len(self.shelfs)):
            shelf_properties = np.array([i])
            shelf_properties = np.append(shelf_properties, self.shelfs[i].x)
            shelf_properties = np.append(shelf_properties, self.shelfs[i].y)
            if (self.shelfs[i].x, self.shelfs[i].y) in self.req_shelfs:
                shelf_properties = np.append(shelf_properties, 1)
            else:
                shelf_properties = np.append(shelf_properties, 0)

            state = np.append(state, shelf_properties)

        if verbose:
            print("Getting the current state")

            for agent in range(len(self.obs)):
                print("\n Observation for Agent {} : {}".format(agent, self.obs[agent]))
            for shelf in range(len(self.shelfs)):
                print("\n Shelfs {}".format(self.shelfs[shelf]))
            print("\n State: ", state)

        return state
    
    def reset_state(self, state):
        self.state = state

    def get_possible_actions(self, verbose=verbose) -> list:
        '''
        Returns the possible actions of the simulation
        '''
        agent_states, shelf_states = self.state_vector_parser(self.state, verbose=verbose)
        possible_actions = []
        for agent in range(len(agent_states)):
            if agent_states[agent][2] == 0:
                possible_actions.append(Actions.PICKUP)

    @staticmethod
    def check_terminal_state(state, verbose=verbose) -> bool:
        '''
        Checks whether the current state is a terminal state

        Parameters
        ----------
        state : np.array
            The current state of the simulation

        Returns
        -------
        bool
            Whether the current state is a terminal state
        '''
        if verbose:
            print("\n Checking whether the current state is a terminal state \n")

        for i in range(2, 3*n_agents, 3):
            if state[i] == 1:
                if (state[i-2], state[i-1]) in goal_coords:
                    return True
        
        return False
    
    @staticmethod
    def state_vector_parser(state, verbose=verbose) -> list:
        '''
        Parses the state vector into a list of agent states and a list of shelf states

        Parameters
        ----------
        state : np.array
            The current state of the simulation

        Returns
        -------
        agent_states : list
            The list of agent states
        shelf_states : list
            The list of shelf states
        '''
        if verbose:
            print("\n Parsing the state vector into a list of agent states and a list of shelf states \n")

        agent_states = np.zeros(shape=(n_agents, 3))
        shelf_states = np.zeros(shape=(int((len(state)-3*n_agents)/2), 3))

        counter = 0
        for i in range(0, 3*n_agents, 3):
            agent_states[counter] = np.array(state[i:i+3])
            counter += 1
        
        counter = 0
        for i in range(3*n_agents, len(state), 3):
            shelf_states[counter] = np.array(state[i:i+3])

        return agent_states, shelf_states