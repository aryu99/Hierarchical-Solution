from config_rl import verbose, goal_coords, Actions, n_agents

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

    if len(action) == 1: # For GOTO GOAL
        goal_pos = goal_coords[1]
        num_steps = abs(agent_pos[0] - goal_pos[0]) + abs(agent_pos[1] - goal_pos[1])
        return num_steps
    
    else:
        if action[0] == Actions.LOAD_FROM_SHELF or action[0] == Actions.UNLOAD_TO_SHELF:
            for shelf in shelfs:
                if shelf.id == action[1]:
                    shelf_pos = (shelf.x, shelf.y)
                    num_steps = (abs(agent_pos[0] - shelf_pos[0]) + abs(agent_pos[1] - shelf_pos[1])) + 1
                    return num_steps





