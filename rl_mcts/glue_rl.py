# from run_search import simulation
import numpy as np
import copy
import numpy as np
import itertools

from abs_sim import AbstractSimulator
from config_rl import env, goal_coords, shelf_coords, verbose

# import sys
# sys.path.append('../../simulation/src')

def get_sim_state(env, verbose=False):
    '''
    Returns the current state of the simulation
    '''
    if verbose:
        print("\n Getting the current state \n")
    obs = env.reset()
    req_queue = env.request_queue

    return obs, req_queue  

obs, req_queue = get_sim_state(env, verbose)
abstract_sim = AbstractSimulator(obs, goal_coords, shelf_coords, req_queue)

def get_current_state():
    '''
    Returns the current state of the simulation
    '''
    print("\n Getting the current state \n")
    return abstract_sim.get_current_state()

def check_terminal_state(state):
    '''
    Returns whether the given state is a terminal state
    '''
    print("\n Checking if the given state is a terminal state \n")
    return abstract_sim.check_terminal_state(state)

# def run_visualizer(game_states, save_to_file=False, saveGS = False):
#     '''
#     Runs the visualizer on the given game states

#     Parameters
#     ----------
#     game_states : list of game states
#         The game states to visualize
#     save_to_file : bool
#         Whether to save the visualization to a file
#     saveGS : bool
#         Whether to save the game states to a pickle file
#     '''
#     if saveGS:
#         simulation.save_to_file('test_0.pkl', gs_list = game_states)
#     print("\n Running the visualizer \n")
#     # visualizer.run(game_states, save_to_file=save_to_file, dir_name = 'W:/Droneconia/simulation/images/test1')

# def run_save(game_states):
#     simulation.save_to_file('test.pkl', gs_list = game_states)
# ------------------------------------------------------------------------------------------------------------------------------

# Simulator API
def GetNextState(CurrState):
    '''
    Returns the next state of the simulation/rollout step in MCTS
    
    Parameters
    ----------
    CurrState : game state

    Returns
    -------
    NextState : game state
    '''
    abstract_sim.reset(CurrState)
    Actions = abstract_sim.get_actions()
    Action = {}

    # Get a random action for each vehicle
    for key,value in Actions.items():
        i = np.random.randint(0, len(value))
        Action[key] = value[i]
    
    # Get the next state
    NextState = abstract_sim.execute_action(Action)  

    return NextState

def EvalNextStates(CurrState):
    '''
    Returns the next children states from a given unexpanded node state in the expansion step of MCTS

    Parameters
    ----------
    CurrState : game state (unexpanded node)

    Returns
    -------
    NextStates : list of game states
    '''
    print("\n Evaluating the new states \n")
    State = copy.deepcopy(CurrState)
    
    abstract_sim.reset(State)
    Actions = abstract_sim.get_actions()

    # Get all possible combinations of actions for all vehicles
    storeActions = []    
    jointActionList = list(Actions.values())
    combinatonList = [p for p in itertools.product(*jointActionList)]
    vehicleList = list(Actions.keys())    
    
    for i in range(len(combinatonList)):
        storeAction = {}
        for j in range(len(vehicleList)):        
            storeAction[vehicleList[j]] = combinatonList[i][j]
        storeActions.append(storeAction)

    # Get the next state for each combination of actions
    NextStates = []
    for m in range(len(storeActions)):
        abstract_sim.reset(State)        
        NextStates.append(abstract_sim.execute_action(storeActions[m])) 

    return NextStates