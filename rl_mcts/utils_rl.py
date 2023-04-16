import time
import os

from config_rl import verbose, goal_coords, Actions, n_agents, MCTS_REWARD_PARAMETER

def state_vector_parser(state, verbose=verbose) -> list:
    '''
    Parses the state vector into a list of agent states and a list of shelf states

    Parameters
    ----------
    state : np.array
        The current state of the simulation

    Returns
    -------
    agent_states : list
        The list of agent states
    shelf_states : list
        The list of shelf states
    '''
    if verbose:
        print("\n Parsing the state vector into a list of agent states and a list of shelf states \n")

    agent_states, shelf_states = [], []

    for i in range(n_agents):
        agent_states.append(state[i])
    
    for j in range(n_agents, len(state)):
        shelf_states.append(state[j])

    return agent_states, shelf_states

# TODO: write a function for estimating which agent reaches first using manhattan distance. Returns the number of steps to complete an action.

def num_steps(state, agent, action:list, verbose=verbose):
    '''
    Returns the number of steps required to complete an action by an agent
    
    Parameters
    ----------
    state : list
        The state of the abstract simulation
        
    agent : Agent
        The agent performing the action
        
    action : list
        The action to be performed by the agent
        
    verbose : bool
        Whether to print the current state of the simulation
    
    Returns
    -------
    num_steps : int
        The number of steps required to complete the action
    '''

    agent_pos = (agent.x, agent.y)
    agents, shelfs = state_vector_parser(state, verbose=verbose)[0], state_vector_parser(state, verbose=verbose)[1] 

    # print("\n ---- Action Received by num_steps: {} ---- \n".format(action))
        
    if action == [Actions.GOTO_GOAL]: # For GOTO GOAL
        # print("\n ---- Printing goal coords in num_steps: {}---- \n".format(goal_coords))
        goal_pos = goal_coords[0]
        num_steps = abs(agent_pos[0] - goal_pos[0]) + abs(agent_pos[1] - goal_pos[1])
        return num_steps
    
    elif action[0] == Actions.LOAD_SHELF: # For LOAD_SHELF
        for shelf in shelfs:
            if shelf.id == action[1]:
                shelf_pos = (shelf.x, shelf.y)
                num_steps = (abs(agent_pos[0] - shelf_pos[0]) + abs(agent_pos[1] - shelf_pos[1])) + 1
                return num_steps
            
    elif action[0] == Actions.UNLOAD_SHELF: # For UNLOAD_SHELF
        for shelf in shelfs:
            if shelf.id == action[1]:
                shelf_pos = shelf.unique_coord
                num_steps = (abs(agent_pos[0] - shelf_pos[0]) + abs(agent_pos[1] - shelf_pos[1])) + 1
                return num_steps

def get_next_coords(x_coord, y_coord, execution_steps, target=goal_coords[0]):
    '''
    Returns the next coordinates of the agent after performing an action for a given number of steps
    
    Parameters
    ----------
    x_coord : int
        The x coordinate of the agent
    y_coord : int
        The y coordinate of the agent
    execution_steps : int
        The number of steps for which the action is to be executed
    target : tuple
        The target coordinates of the agent
    
    Returns
    -------
    x_coord : int
        The x coordinate of the agent after performing the action for the given number of steps
    y_coord : int
        The y coordinate of the agent after performing the action for the given number of steps
    '''
    available_steps = execution_steps

    goal_pos = target
    agent_x = x_coord
    agent_y = y_coord
    
    while available_steps > 0:
        if agent_y < goal_pos[1]:
            agent_y += 1
            available_steps -= 1
        elif (agent_y > goal_pos[1]) and (available_steps > 0):
            agent_y -= 1
            available_steps -= 1
        if (agent_x < goal_pos[0]) and (available_steps > 0):
            agent_x += 1
            available_steps -= 1
        elif (agent_x > goal_pos[0]) and (available_steps > 0):
            agent_x -= 1
            available_steps -= 1

    return agent_x, agent_y


def calc_rollout_reward(state, reward_format=MCTS_REWARD_PARAMETER.value):

    if reward_format == 0:
        reward = 0
        goal_pos = goal_coords[0]
        agents, shelfs = state_vector_parser(state, verbose=verbose)[0], state_vector_parser(state, verbose=verbose)[1]

        for agent in agents:
            pos_x, pos_y = agent.x, agent.y
            if (pos_x, pos_y) == goal_pos and agent.shelf != 0:
                reward += 1
            else:
                if agent.flag == 1 and agent.shelf != 0 and agent.action != None and agent.action[0].value == 2:
                    reward += 0.2
        return reward

    elif reward_format == 1:
        reward = 0
        goal_pos = goal_coords[0]
        agents, shelfs = state_vector_parser(state, verbose=verbose)[0], state_vector_parser(state, verbose=verbose)[1]

        for agent in agents:
            pos_x, pos_y = agent.x, agent.y
            if (pos_x, pos_y) == goal_pos and agent.shelf != 0:
                pass
            else:
                if agent.flag == 1 and agent.shelf != 0 and agent.action != None and agent.action[0].value == 2:
                    reward += 1/(abs(pos_x - goal_pos[0]) + abs(pos_y - goal_pos[1]))
        return reward


def saveText(Text, name="final_result"):
    '''
    Saves the result of the game to a text file

    Parameters
    ----------
    Text : whatever you want to save, gets converted to string within this function (for example, result of the game)
    name : String (name of the file)
    '''
    filename = name + ".txt"
    if os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    f = open(filename, append_write)
    f.write(str(Text) + '\n')
    f.close()

def timer():
    '''
    Returns the current time in seconds
    
    Returns
    -------
    time : float
        The current time in seconds
    '''
    return time.time()

def print_state(state):
    '''
    Prints the current state of the simulation
    
    Parameters
    ----------
    state : list
        The state of the abstract simulation
    '''
    str_store = []
    for entity in state:
        str_store.append(str(entity))
    return str_store


def format_actions(actions_list, shelfs): 

    formatted_actions_list = []
    for action_dict in actions_list:
        action_pair = []
        for action in list(action_dict.values()):
            action_desc = []
            action_desc.append(action[0].value)
            if len(action) == 2:
                for shelf in shelfs:
                    if shelf.id == action[1]:
                        action_desc.append((shelf.x, shelf.y))
            action_pair.append(action_desc)
        formatted_actions_list.append(action_pair)

    return formatted_actions_list
                
            




    
    
        





