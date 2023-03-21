import numpy as np
from enum import Enum
import copy

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
        Returns the current state of the simulation as a vector of Agent and Shelf objects
        '''

        state = []

        for i in range(len(self.obs)):
            state.append(Agent(i+1, self.obs[i][0], self.obs[i][1], self.obs[i][2], 0))
        # print("\n -----------\n printing requested shelfs: {} \n -----------\n".format(self.req_shelfs))

        requested_shelf_coords = []
        for req_shelf in self.req_shelfs:
            requested_shelf_coords.append((req_shelf.x, req_shelf.y))

        for i in range(len(self.shelfs)):
            if (self.shelfs[i].x, self.shelfs[i].y) in requested_shelf_coords:
                state.append(Shelf(i+1, self.shelfs[i].x, self.shelfs[i].y, 1, 0))
            else:
                state.append(Shelf(i+1, self.shelfs[i].x, self.shelfs[i].y, 0, 0))

        if verbose:
            print("Getting the current state")

            for agent in range(len(self.obs)):
                print("\n Observation for Agent {} : {}".format(agent, self.obs[agent]))
            for shelf in range(len(self.shelfs)):
                print("\n Shelfs {}".format(self.shelfs[shelf]))
            print("\n State: ", state)

        return state
    
    def get_current_state(self):
        return self.state
    
    def reset_state(self, state):
        self.state = state

    def get_actions(self, verbose=verbose) -> dict:
        '''
        Returns the possible actions of the simulation

        TODO: Add a continue action for agent whose action execution is in progress
        '''
        agent_states, shelf_states = utils_rl.state_vector_parser(self.state, verbose=verbose)[0], utils_rl.state_vector_parser(self.state, verbose=verbose)[1]
        possible_actions = {}
        for agent in agent_states:
            action_list = []

            if agent.action != None: # Action: CONTINUE
                action_list.append([Actions.CONTINUE])
                possible_actions[agent] = action_list
                continue

            elif agent.shelf == 0: # Action: LOAD_SHELF
                for shelf in shelf_states:
                    for action in action_list:
                        if action == [Actions.LOAD_SHELF, shelf.id]:
                            continue
                    if shelf.req == 1 and shelf.pos == 0:
                        action_list.append([Actions.LOAD_SHELF, shelf.id])                     
                possible_actions[agent] = action_list
                continue

            elif agent.shelf != 0 and agent.flag == 1: # Action: GOTO_GOAL and UNLOAD_SHELF (For now can only unload a req shelf)
                action_list.append([Actions.GOTO_GOAL])
                store_static_shelf_pos = []
                for shelf in shelf_states:
                    if shelf.pos == 0:
                        store_static_shelf_pos.append([shelf.x, shelf.y])
                
                for shelf in shelf_states:
                    if shelf.pos != 0:
                        if shelf.unique_coord in store_static_shelf_pos:
                            continue
                        else:
                            action_list.append([Actions.UNLOAD_SHELF, shelf.id])
                possible_actions[agent] = action_list
                continue

            elif agent.shelf != 0 and agent.flag == 0: # Action: UNLOAD_SHELF
                store_static_shelf_pos = []
                for shelf in shelf_states:
                    if shelf.pos == 0:
                        store_static_shelf_pos.append([shelf.x, shelf.y])
                
                for shelf in shelf_states:
                    if shelf.pos != 0:
                        if shelf.unique_coord in store_static_shelf_pos:
                            continue
                        else:
                            action_list.append([Actions.UNLOAD_SHELF, shelf.id])
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

        TODO: Add a continue action for agent whose action execution is in progress

        Need to make two loops. First loop figures out the number of steps required for each agent to complete action. 
        Second loop executes the action conditioned on the stored number of steps.
        '''
        if verbose:
            print("\n Executing action {} \n".format(actions))

        store_num_steps = {}
        store_actions_steps = {}

        agents, shelfs = utils_rl.state_vector_parser(self.state, verbose=verbose)

        # This loop figures out the number of steps required for each agent to complete action
        for key, value in actions.items():
            for agent in agents:
                print("\n Agent: {}, Key: {}".format(agent, key))
                if agent.id == key.id:
                    store_num_steps[key] = utils_rl.num_steps(self.state, key, value)
                    store_actions_steps[key] = [value, store_num_steps[key]]

        min_steps_val = min(store_num_steps.values())
        

        # This loop executes the action conditioned on the stored number of steps
        for key, value in store_actions_steps.items():
            if value[0] == [Actions.GOTO_GOAL]: # Action: GOTO_GOAL
                for agent in agents:
                    if agent.id == key.id:
                        assert key.shelf != 0, "For Action: GOTO_GOAL, the agent should have a shelf"
                        assert key.flag == 1, "For Action: GOTO_GOAL, the agent should have a shelf that has content requested"
                        if value[1] == min_steps_val:
                            agent.x, agent.y = goal_coords[0]
                            agent.toggle_flag()
                            for shelf in shelfs:
                                if shelf.id == key.shelf:
                                    shelf.req = 0
                        else:
                            available_steps = value[1] - min_steps_val
                            agent.x, agent.y = utils_rl.get_next_coords(agent.x, agent.y, available_steps)    
                    break
                continue


            elif value[0][0] == Actions.LOAD_SHELF: # Action: LOAD_SHELF
                for agent in agents:
                    if agent.id == key.id:
                        assert key.shelf == 0, "For Action: LOAD_SHELF, the agent should not have a shelf"
                        assert key.flag == 0, "For Action: LOAD_SHELF, as the agent does not have any shelf, the flag should be 0"
                        
                        for shelf in shelfs:
                            if shelf.id == value[0][1]:
                                # For simplification, we assume that the agent only picks up shelf that is requested 
                                assert shelf.req == 1, "For Action: LOAD_SHELF, the shelf should be a requested shelf"
                                assert shelf.pos == 0, "For Action: LOAD_SHELF, the shelf should be at a shelf position"
                                if value[1] == min_steps_val:
                                    agent.shelf = shelf.id
                                    agent.flag = shelf.req
                                    assert agent.flag == 1, "For Action: LOAD_SHELF, the flag should be 1 after the agent picks the shelf"
                                    shelf.pos = copy.deepcopy(agent.id)
                                    shelf.x, shelf.y = copy.deepcopy(agent.x), copy.deepcopy(agent.y)

                                else:
                                    available_steps = value[1] - min_steps_val
                                    agent.x, agent.y = utils_rl.get_next_coords(agent.x, agent.y, available_steps, target=(shelf.x, shelf.y))
                            break
                    break
                continue

            elif value[0][0] == Actions.UNLOAD_SHELF: # Action: UNLOAD_SHELF (For now can unload a requested shelf also)
                for agent in agents:
                    if agent.id == key.id:
                        assert key.shelf != 0, "For Action: UNLOAD_SHELF, the agent should have a shelf"
                        
                        for shelf in shelfs:
                            if shelf.id == value[0][1]:
                                if value[1] == min_steps_val:
                                    agent.shelf = 0
                                    agent.flag = 0
                                    shelf.pos = 0
                                    shelf.x, shelf.y = agent.x, agent.y
                                else:
                                    available_steps = value[1] - min_steps_val
                                    agent.x, agent.y = utils_rl.get_next_coords(agent.x, agent.y, available_steps, target=(shelf.x, shelf.y))
                            break
                    break
                continue

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
            
        # print("\n Current state: {} \n".format(state))
        agents, shelfs = utils_rl.state_vector_parser(state, verbose=verbose)

        req_counter = 0
        for shelf in shelfs:
            if shelf.req == 1:
                req_counter += 1

        if req_counter < n_requests:
            return True
        else:
            return False

