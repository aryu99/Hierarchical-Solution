from enum import Enum
import gym

import sys
sys.path.append('../../robotic_warehouse/')

import rware

# Global verbose
verbose = False


# --------------------
# Abstract Sim stuff

class Actions(Enum):
    '''
    Enum for the actions
    '''
    LOAD_SHELF = 0
    UNLOAD_SHELF = 1
    GOTO_GOAL = 2
    DO_NOTHING = 3
    

n_agents = 2
n_requests = 2
sensor_range = 9
default_layout = """
.........
.x.....x.
.........
.........
....x....
.........
.........
.........
....g....
"""


def make_env():
    env = gym.make("rware-tiny-2ag-v1", sensor_range=sensor_range, request_queue_size=n_requests, n_agents=n_agents, layout=default_layout, training_mode = False)
    return env

def get_goal_coords(init_env, verbose=False):
    '''
    Returns the goal coordinates of the environment
    '''
    if verbose:
        print("\n Getting the goal coordinates \n")
    goal_coords = init_env.goals

    return goal_coords

def get_shelf_coords(init_env, verbose=False):
    '''
    Returns the coordinates of the shelves in the environment
    '''
    if verbose:
        print("\n Getting the shelf coordinates \n")
    init_env.reset()
    shelf_coords = init_env.shelfs

    return shelf_coords

goal_coords = get_goal_coords(make_env(), verbose)
shelf_coords = get_shelf_coords(make_env(), verbose)


# ---------------------------------------------
# MCTS stuff

class RewardFormat(Enum):
    '''
    Enum for the reward format

    TERMINAL: Preset Reward is given after seeng the state after a set number of rollout steps
    INVERSE: Reward is inversely proportional to the number of rollout steps it takes to reach the terminal state
    '''
    TERMINAL = 0
    INVERSE = 1

MCTS_REWARD_PARAMETER = RewardFormat.INVERSE
MCTS_ROLLOUT_STEPS = 2
MCTS_SIM_PARALLEL_ROLLOUT_NUM = 10
MAX_ITERATIONS_PER_ACTION = 1000

# ---------------------------------------------


