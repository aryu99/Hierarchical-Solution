import glue_rl
import time
import utils_rl
import numpy as np
import abs_sim

from config import n_agents, n_requests, default_layout, env, verbose, goal_coords, shelf_coords

if __name__ == "__main__":

    # setting up the environment
    obs, req_queue = glue_rl.get_sim_state(env, verbose)
    abstract_sim = abs_sim.AbstractSimulator(obs, goal_coords, shelf_coords, req_queue)
    root_state = abs_sim.get_vector_state(obs, req_queue)
    print(root_state)
    # print(goal_coords)
    # print(utils_rl.check_terminal_state(root_state))
    print(utils_rl.state_vector_parser(root_state))
    # print(req_queue[0].x)
    # print(env.get_action_space())
    # print(obs)

    # env.render()
    # time.sleep(5)

