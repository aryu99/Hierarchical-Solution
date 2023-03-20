import time
import numpy as np
import copy

import utils_rl
import glue_rl
import node_rl

from config_rl import n_agents, n_requests, default_layout, env, verbose, goal_coords, shelf_coords

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

    # setting up the environment
    # obs, req_queue = glue_rl.get_sim_state(env, verbose)
    # abstract_sim = abs_sim.AbstractSimulator(obs, goal_coords, shelf_coords, req_queue)
    root_state = copy.deepcopy(glue_rl.get_current_state())
    root_node = node_rl.Node(root_state)
    print(root_state)
    # print(goal_coords)
    # print(utils_rl.check_terminal_state(root_state))
    print(utils_rl.state_vector_parser(root_state))
    # print(req_queue[0].x)
    # print(env.get_action_space())
    # print(obs)
    gameStates = sol.storeGameStates
    # env.render()
    # time.sleep(5)

