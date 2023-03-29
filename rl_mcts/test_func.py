'''
Script to test get_actions and execute_action functions
'''

import utils_rl as utils
from entities_rl import Agent, Shelf
from abs_sim import AbstractSimulator
from config_rl import Actions
import glue_rl

test_flag = 2


def create_state():
    # Create a state with two agents and three shelfs

    # agent_1 pos = (3,7)
    # agent_2 pos = (5,7)

    agent_1 = Agent(1, 3, 7, 0, 0)
    agent_2 = Agent(2, 4, 7, 0, 0)
    # agent_2.action = [Actions.UNLOAD_SHELF, 2]
    
    # shelf_1 = (1,1) - req
    # shelf_2 = (7,1) - req
    # shelf_3 = (4,4)

    shelf_1 = Shelf(1, 1, 1, 1, 0)
    # shelf_1.pos = 1
    # shelf_1.x = 4
    # shelf_1.y = 5
    shelf_2 = Shelf(2, 7, 1, 1, 0)
    # shelf_2.x = 4
    # shelf_2.y = 8
    # shelf_2.pos = 2
    shelf_3 = Shelf(3, 4, 4, 0, 0)

    state = [agent_1, agent_2, shelf_1, shelf_2, shelf_3]
    return state



if __name__ == "__main__":
    
    if test_flag == 0:
        possible_actions = AbstractSimulator.get_actions(create_state())
        # print(possible_actions)

    elif test_flag == 1:

        agent_1 = Agent(1, 1, 1, 1, 0)
        agent_2 = Agent(2, 7, 1, 2, 0)

        # Test execute_action
        state = create_state()
        actions = {}
        actions[agent_1] = [Actions.DO_NOTHING]
        actions[agent_2] = [Actions.UNLOAD_SHELF, 2]
        AbstractSimulator.execute_action(state, actions)
        # print("action: {}".format(action))
        # print("state: {}".format(state))
        # print("num_steps: {}".format(utils.num_steps(state, state[0], action)))
        # print("next_coords: {}".format(utils.get_next_coords(state[0].x, state[0].y, utils.num_steps(state, state[0], action))))
        # print("execute_action: {}".format(abs_sim.execute_action(state, action)))

    elif test_flag == 2:
        state = create_state()
        NextStates = glue_rl.EvalNextStates(state)
        state_counter = 0
        for state in NextStates:
            print("\n Printing State No. {}".format(state_counter))
            for entity in state[0]:
                print("\n", entity)

            state_counter += 1





