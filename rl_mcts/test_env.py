# from enum import Enum
# import gym

# import sys
# sys.path.append('../../robotic_warehouse/')

# # import rware
# from rware.warehouse import ObserationType

# verbose = False


# # --------------------
# # Abstract Sim stuff

# # class Actions(Enum):
# #     '''
# #     Enum for the actions
# #     '''
# #     LOAD_SHELF = 0
# #     UNLOAD_SHELF = 1
# #     GOTO_GOAL = 2
# #     CONTINUE = 3
# #     # DO_NOTHING = 3
    

# n_agents = 3
# n_requests = 2
# sensor_range = 9
# default_layout = """
# .........
# .x.....x.
# .........
# ....x....
# .........
# .........
# .........
# ....g....
# """

# env = gym.make("rware:rware-tiny-4ag-v1", sensor_range=sensor_range, request_queue_size=n_requests, n_agents=n_agents, layout=default_layout, observation_type=ObserationType.FLATTENED)
# env.reset()

# # def get_goal_coords(env, verbose=False):
# #     '''
# #     Returns the goal coordinates of the environment
# #     '''
# #     if verbose:
# #         print("\n Getting the goal coordinates \n")
# #     goal_coords = env.goals

# #     return goal_coords

# # def get_shelf_coords(env, verbose=False):
# #     '''
# #     Returns the coordinates of the shelves in the environment
# #     '''
# #     if verbose:
# #         print("\n Getting the shelf coordinates \n")
# #     shelf_coords = env.shelfs

# #     return shelf_coords

# # goal_coords = get_goal_coords(env, verbose)
# # shelf_coords = get_shelf_coords(env, verbose)


# # # ---------------------------------------------
# # # MCTS stuff

# # class RewardFormat(Enum):
# #     '''
# #     Enum for the reward format

# #     TERMINAL: Preset Reward is given after seeng the state after a set number of rollout steps
# #     INVERSE: Reward is inversely proportional to the number of rollout steps it takes to reach the terminal state
# #     '''
# #     TERMINAL = 0
# #     INVERSE = 1

# # MCTS_REWARD_PARAMETER = RewardFormat.TERMINAL
# # MCTS_ROLLOUT_STEPS = 10

# # ---------------------------------------------

# import gym
# import rware

default_layout = """
.........
.x.....x.
.........
....x....
.........
.........
.........
....g....
"""
# env = gym.make("rware:rware-tiny-2ag-v1", layout=default_layout)
# print(env.n_agents)  # 2
# print(env.action_space)  # Tuple(Discrete(5), Discrete(5))
# print(env.observation_space)  # Tuple(Box(XX,), Box(XX,))
# # obs = env.reset()

import gym


import sys
sys.path.append('../../robotic_warehouse')

import rware
# from rware.warehouse import ObserationType

env = gym.make("rware-tiny-2ag-v1", n_agents=2)
obs = env.reset()
# done = [False] * env.n_agents
# while not all(done):
# actions = env.action_space.sample()
# next_obs, reward, done, info = env.step(actions)
# env.render()
# env.close()
