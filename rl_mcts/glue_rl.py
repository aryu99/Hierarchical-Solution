# from run_search import simulation
import numpy as np
import copy
import numpy as np
import itertools

from config_rl import env, goal_coords, shelf_coords, verbose, Actions
from abs_sim import AbstractSimulator
import utils_rl


# import sys
# sys.path.append('../../simulation/src')

def get_sim_state(env, verbose=False):
    '''
    Returns the current state of the simulation
    '''
    if verbose:
        print("\n Getting the sim state \n")
    obs = env.reset()
    req_queue = env.request_queue

    return obs, req_queue  

obs, req_queue = get_sim_state(env, verbose)
abstract_sim = AbstractSimulator(obs, goal_coords, shelf_coords, req_queue)

def get_current_state():
    '''
    Returns the current state of the simulation
    '''
    if verbose:
        print("\n Getting the current state \n")
    return abstract_sim.get_current_state()

def check_terminal_state(state):
    '''
    Returns whether the given state is a terminal state
    '''
    if verbose:
        print("\n Checking if the given state is a terminal state \n")
    return abstract_sim.check_terminal_state(state)

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
    # print(type(CurrState))
    print("\n ---printing getNexState State--- \n")
    for entity in CurrState:
        print(entity)
    abstract_sim.reset_state(CurrState)
    Actions = abstract_sim.get_actions()
    print("GetActions in GetNextState: {}".format(Actions))
    Action = {}

    # Get a random action for each vehicle
    if len(Action)==0:
        while all(x == list(Action.values())[0] for x in Action.values()):
            Action = {}
            for key,value in Actions.items():
                i = np.random.randint(0, len(value))
                Action[key] = value[i]
        
        # print("while loop condition: {}; Action 1: {}, Action 2 : {}".format(list(Action.values())[0], list(Action.values())[1], list(Action.values())[0][0].value,  == list(Actions.values())[1])) 
    
    print("Action in GetNextState: Act_1: {}, Act_2: {}".format(list(Action.values())[0], list(Actions.values())[1]))
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
    if verbose:
        print("\n Evaluating the new states \n")
    State = copy.deepcopy(CurrState)
    
    abstract_sim.reset_state(State)
    Actions = abstract_sim.get_actions()

    # Get all possible combinations of actions for all vehicles
    storeActions = []    
    jointActionList = list(Actions.values())
    combinatonList = [p for p in itertools.product(*jointActionList)]
    AgentList = list(Actions.keys())    

    
    for i in range(len(combinatonList)):
        storeAction = {}
        for j in range(len(AgentList)):        
            storeAction[AgentList[j]] = combinatonList[i][j]
        storeActions.append(storeAction)

    # Get the next state for each combination of actions
    NextStates = []
    # counter = 0
    # for agent_action in storeActions:
    #     counter += 1
    #     for key,value in agent_action.items():
            # print("\n ---Printing storeAction {} Agent: {}, Action executed: {}  \n".format(counter, key, value))

    print("\n ---Printing storeActions: {} \n".format(storeActions))
    for m in range(len(storeActions)):
        # check if all values are same in the dictionary
        if all(x == list(storeActions[m].values())[0] for x in storeActions[m].values()):
            print("All values are same in the dictionary, hence skipping this action {}, {}".format(storeActions[m], list(storeActions[m].values())[0]))
            continue
        abstract_sim.reset_state(copy.deepcopy(State))      
        # print("\n ---Printing Action getting executed: {} \n".format(storeActions[m]))  
        for key,value in storeActions[m].items():
            print("\n ---Printing execution Agent: {}, Action executed: {}  \n".format(key, value))
        # print("\n printing the state returned by execute action \n")
        # utils_rl.print_state(abstract_sim.execute_action(storeActions[m]))
        NextStates.append((abstract_sim.execute_action(storeActions[m]), storeActions[m])) 
    for state in NextStates:
        print("\n ---Printing NextStates: {} \n".format(state))
        for entity in state[0]:
            print("--- Using EvalNextStates State Entity: {}---".format(entity))
    return NextStates