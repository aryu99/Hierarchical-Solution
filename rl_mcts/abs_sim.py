import numpy as np
from enum import Enum

from config_rl import n_agents, n_requests, default_layout, verbose, goal_coords, shelf_coords, Actions
from entities_rl import Agent, Shelf
import utils_rl
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
            state = state.append(Agent(i+1, self.obs[i][0], self.obs[i][1], self.obs[i][2], 0))

        for i in range(len(self.shelfs)):
            if (self.shelfs[i].x, self.shelfs[i].y) in self.req_shelfs:
                state = state.append(Shelf(i+1, self.shelfs[i].x, self.shelfs[i].y, 1, 0))
            else:
                state = state.append(Shelf(i+1, self.shelfs[i].x, self.shelfs[i].y, 0, 0))

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
        agent_states, shelf_states = utils_rl.state_vector_parser(self.state, verbose=verbose)[0], utils_rl.state_vector_parser(self.state, verbose=verbose)[1]
        possible_actions = {}
        for agent in range(len(agent_states)):
            action_list = []

            if agent_states[agent][3] == 0:
                for shelf in range(len(shelf_states)):
                    if shelf.req == 1 and shelf.pos == 0:
                        action_list.append([Actions.LOAD_FROM_SHELF, shelf.id])                     
                possible_actions[agent] = action_list
                continue
            
            # if agent_states[agent][3] == 0:
            #     for shelf in range(len(shelf_states)):
            #         if shelf.req == 1 and shelf.pos != 0:
            #             action_list.append([Actions.DO_NOTHING])                     
            #     possible_actions[agent] = action_list
            #     continue

            elif agent_states[agent][3] != 0 and agent_states[agent][4] == 1:
                action_list.append([Actions.GOTO_GOAL])
                for shelf in range(len(shelf_states)):
                    if shelf.pos != 0:
                        action_list.append([Actions.UNLOAD_TO_SHELF, shelf.id])
                possible_actions[agent] = action_list
                continue

            elif agent_states[agent][3] != 0 and agent_states[agent][4] == 0:
                for shelf in range(len(shelf_states)):
                    if shelf.pos != 0:
                        action_list.append([Actions.UNLOAD_TO_SHELF, shelf.id])
                possible_actions[agent] = action_list
                continue

        if verbose:
            print("\n Possible actions: ", possible_actions)
        
        return possible_actions
                
            
    def execute_action(self, actions, verbose=verbose) -> np.array:
        '''
        Executes the action in the simulation. Also figures out which agent completes action first

        Parameters
        ----------
        action : Dict
            The action to be executed

        Returns
        -------
        np.array
            The new state of the simulation
        '''
        if verbose:
            print("\n Executing action {} \n".format(actions))

        store_num_steps = {}

        agents, shelfs = utils_rl.state_vector_parser(self.state, verbose=verbose)

        for key, value in actions.items():
            if len(value) == 1: # Action: GOTO_GOAL
                assert key.shelf != 0
                assert key.flag == 1
                store_num_steps[key] = utils_rl.num_steps(self.state, key, value)
                for agent in agents:
                    if agent.id == key.id:
                        agent.x, agent.y = goal_coords[1]




            if value[0] == Actions.LOAD_FROM_SHELF:
                self.state[key][3] = 1
                self.state[value[1]][2] = 0
                self.state[value[1]][3] = 1
            elif value[0] == Actions.UNLOAD_TO_SHELF:
                self.state[key][3] = 0
                self.state[key][4] = 1
                self.state[value[1]][2] = 1
                self.state[value[1]][3] = 0
            elif value[0] == Actions.GOTO_GOAL:
                self.state[key][4] = 0


    @staticmethod
    def check_terminal_state(state, verbose=verbose) -> bool:
        '''
        Checks whether the current state is a terminal state. Does so by checking if 
        the requested number of shelfs is n_req - 1 by going through all shelfs.

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

