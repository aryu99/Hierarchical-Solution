import time
import numpy as np
import copy
from MCTS_rl import MCTS

import utils_rl
import glue_rl
import node_rl

# from config_rl import n_agents, n_requests, default_layout, env, verbose, goal_coords, shelf_coords

# Modifiable variables for MCTS
MaxIteration = 10 #maximum number of iterations for selecting one action
numActions = 50 # number of actions to be selected



def train_rl_subcontrollers():
    '''
    Train all the RL Subcontrollers
    '''
    print("Training all the RL Subcontrollers")
    pass

def run_MCTS():
    '''
    Run the MCTS solution until something gets delivered
    '''
    print("Running the MCTS solution until something gets delivered")
    root_state = copy.deepcopy(glue_rl.get_current_state())
    root_node = node_rl.Node(root_state)
    root_node.visits = 1

    sol = MCTS(root_node)
    time = utils_rl.timer()
    sol.Run(MaxIteration, numActions, del_children=True, limit_del = True, clear_root=False)
    end_time = utils_rl.timer()
    print("Time taken: ", end_time - time)
    gameStates = sol.storeGameStates
    actions = sol.storeActions
    # print(gameStates)
    state_count = 0
    print("\n printing gameStates: \n")
    for state in gameStates:
        state_count += 1
        print("\n State: {}".format(state_count))
        for entity in state:
            print(entity)
    print("\n printing actions: \n")
    for action in actions:
        print(action)

    
    # print(actions)
    pass

if __name__ == "__main__":

    '''
    Flow:
    1. Train all the RL Subcontrollers
    2. Run the MCTS solution until something gets delivered
    3. Execute the RL subcontrollers as required by MCTS until you get a new request
    4. Repeat from step 2
    '''

    # TODO: Write loop to train all the RL Subcontrollers

# ----------------------------------------------------------------
    # Loop to run the MCTS solution

    run_MCTS()
    # setting up the environment
    # obs, req_queue = glue_rl.get_sim_state(env, verbose)
    # abstract_sim = abs_sim.AbstractSimulator(obs, goal_coords, shelf_coords, req_queue)
    
    # print(goal_coords) 
    # print(utils_rl.check_terminal_state(root_state))\
    # print(req_queue[0].x)
    # print(env.get_action_space())
    # print(obs)
    
    # env.render()
    # time.sleep(5)

