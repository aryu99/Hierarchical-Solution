import time

from config_rl import verbose, goal_coords, Actions, n_agents, MCTS_REWARD_PARAMETER, RewardFormat

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
        agent_states.append(i)
    
    for i in range(n_agents, len(state)):
        shelf_states.append(i)

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

    continue_flag = 0

    if action == [Actions.CONTINUE]:
        if agent.action == Actions.GOTO_GOAL:
            continue_flag = 1
        
        elif agent.action in [Actions.LOAD_SHELF, Actions.UNLOAD_SHELF]:
            continue_flag = 2 
        
    if action == [Actions.GOTO_GOAL] or continue_flag == 1: # For GOTO GOAL
        goal_pos = goal_coords[1]
        num_steps = abs(agent_pos[0] - goal_pos[0]) + abs(agent_pos[1] - goal_pos[1])
        return num_steps
    
    elif action[0] == Actions.LOAD_SHELF or action[0] == Actions.UNLOAD_SHELF or continue_flag == 2: # For LOAD_FROM_SHELF or UNLOAD_TO_SHELF
        for shelf in shelfs:
            if shelf.id == action[1]:
                shelf_pos = (shelf.x, shelf.y)
                num_steps = (abs(agent_pos[0] - shelf_pos[0]) + abs(agent_pos[1] - shelf_pos[1])) + 1
                return num_steps

def get_next_coords(x_coord, y_coord, execution_steps, target=goal_coords[1]):
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
        elif agent_y > goal_pos[1]:
            agent_y -= 1
            available_steps -= 1
        if agent_x < goal_pos[0]:
            agent_x += 1
            available_steps -= 1
        elif agent_x > goal_pos[0]:
            agent_x -= 1
            available_steps -= 1
        
    return agent_x, agent_y


def calc_rollout_reward(state, reward_format=MCTS_REWARD_PARAMETER):

    if reward_format == RewardFormat.TERMINAL:
        assert len(state)==1
        return 

    elif reward_format == RewardFormat.INVERSE:
        assert len(state)==2, "Input should be state vector and num of steps taken to reach the terminal state"


def saveText(filename, text):
    '''
    Saves a text file with the given filename and text
    
    Parameters
    ----------
    filename : str
        The name of the file to be saved
    text : str
        The text to be saved in the file
    '''
    with open(filename, 'w') as f:
        f.write(text)

def timer():
    '''
    Returns the current time in seconds
    
    Returns
    -------
    time : float
        The current time in seconds
    '''
    return time.time()

        




    
    
        





