'''
Script to test get_actions and execute_action functions
'''

import utils_rl as utils
from entities_rl import Agent, Shelf
import abs_sim
from config_rl import Actions

test_flag = 0

def create_state():
    # Create a state with two agents and three shelfs

    # agent_1 pos = (3,7)
    # agent_2 pos = (5,7)

    agent_1 = Agent(1, 3, 7, 0, 0)
    agent_2 = Agent(2, 5, 7, 0, 0)

    
    # shelf_1 = (1,1) - req
    # shelf_2 = (7,1) - req
    # shelf_3 = (4,4)

    shelf_1 = Shelf(1, (1,1), 1, 1, 1, 0)
    shelf_2 = Shelf(2, (7,1), 7, 1, 1, 0)
    shelf_3 = Shelf(3, (4,4), 4, 4, 0, 0)

    state = [agent_1, agent_2, shelf_1, shelf_2, shelf_3]
    return state



if __name__ == "__main__":
    
    if test_flag == 0:
        possible_actions = abs_sim.get_actions(create_state())
        print(possible_actions)

    elif test_flag == 1:
        




