import numpy as np
from enum import Enum

from config_rl import n_agents, n_requests, default_layout, verbose, goal_coords, shelf_coords, Actions
from entities_rl import Agent, Shelf
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

        state = []

        for i in range(len(self.obs)):
            state = state.append(Agent(i, self.obs[i][0], self.obs[i][1], self.obs[i][2], 0))

        for i in range(len(self.shelfs)):
            if (self.shelfs[i].x, self.shelfs[i].y) in self.req_shelfs:
                state = state.append(Shelf(i, self.shelfs[i].x, self.shelfs[i].y, 1, 0))
            else:
                state = state.append(Shelf(i, self.shelfs[i].x, self.shelfs[i].y, 0, 0))

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

    def get_actions(self, verbose=verbose) -> list:
        '''
        Returns the possible actions of the simulation
        '''
        agent_states, shelf_states = self.state_vector_parser(self.state, verbose=verbose)[0], self.state_vector_parser(self.state, verbose=verbose)[1]
        possible_actions = {}
        for agent in range(len(agent_states)):
            action_list = []
            if agent_states[agent][3] == 0:
                for shelf in range(len(shelf_states)):
                    if shelf.req == 1 and shelf.pos == 0:
                        action_list.append([Actions.LOAD_FROM_SHELF, shelf.id])                     
                possible_actions[agent] = action_list
                continue

            elif agent_states[agent][3] != 0 and agent_states[agent][4] == 1:
                action_list.append(Actions.GOTO_GOAL)
                for shelf in range(len(shelf_states)):
                    if shelf.pos == 1:
                        action_list.append([Actions.UNLOAD_TO_SHELF, shelf.id])
                possible_actions[agent] = action_list
                continue

            elif agent_states[agent][3] != 0 and agent_states[agent][4] == 0:
                for shelf in range(len(shelf_states)):
                    if shelf.pos == 1:
                        action_list.append([Actions.UNLOAD_TO_SHELF, shelf.id])
                possible_actions[agent] = action_list
                continue

        if verbose:
            print("\n Possible actions: ", possible_actions)
        
        return possible_actions
                
            
    def execute_action(self, action, verbose=verbose) -> np.array:
        '''
        Executes the action in the simulation

        Parameters
        ----------
        action : int
            The action to be executed

        Returns
        -------
        np.array
            The new state of the simulation
        '''
        if verbose:
            print("\n Executing action {} \n".format(action))

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

        agent_states, shelf_states = [], []

        for i in range(n_agents):
            agent_states.append(i)
        
        for i in range(n_agents, len(state)):
            shelf_states.append(i)

        return agent_states, shelf_states