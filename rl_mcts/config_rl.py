from enum import Enum
import gym

import sys
sys.path.append('../robotic_warehouse/')

import rware
import glue_rl

class RewardFormat(Enum):
    '''
    Enum for the reward format
    '''
    TERMINAL = 0
    INVERSE = 1

class Actions(Enum):
    '''
    Enum for the actions
    '''
    LOAD_FROM_SHELF = 0
    UNLOAD_TO_SHELF = 1
    GOTO_GOAL = 2
    

n_agents = 2
n_requests = 2
sensor_range = 9
default_layout = """
.........
.x.....x.
.........
....x....
.........
.........
.........
...ggg...
"""

verbose = False
MCTS_REWARD_PARAMETER = RewardFormat.TERMINAL

env = gym.make("rware-tiny-2ag-v1", sensor_range=sensor_range, request_queue_size=n_requests, n_agents=n_agents, layout=default_layout)

goal_coords = glue_rl.get_goal_coords(env, verbose)
shelf_coords = glue_rl.get_shelf_coords(env, verbose)