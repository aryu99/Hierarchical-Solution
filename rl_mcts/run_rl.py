import time
import copy

from low_level_controller.rl_controller import RLController

import utils_rl
import glue_rl
import node_rl
from config_rl import MAX_ITERATIONS_PER_ACTION, Actions
from MCTS_rl import MCTS



# Modifiable variables for MCTS
MaxIteration = MAX_ITERATIONS_PER_ACTION #maximum number of iterations for selecting one action

def load_and_demonstrate(controller_name):
    '''
    Load a saved RLController and demonstrate its capabilities

    Parameters
    ----------
    controller_name : str
        The name of the controller to be loaded
    '''
    path = "saved_controllers"
    subcontroller = RLController(0, 0, training_mode=True, max_training_steps=100, verbose=True)
    subcontroller.load(path)
    subcontroller.demonstrate_capabilities(n_episodes=3)

def train_rl_subcontrollers():
    '''
    Train all the RL Subcontrollers

    Note: For now idx of subcontroller corresponds to the action value that it represents.
    '''
    count = 0
    MAX_TRAINING_STEPS = 1000 #30
    TIMESTEPS =  3e6 #3e5 #5e4
    for action in Actions:
        count += 1
        print(action)
        subcontroller = RLController(action.value, action.value, training_mode=True, max_training_steps=MAX_TRAINING_STEPS, verbose=True)
        subcontroller.learn(total_timesteps=TIMESTEPS)
        if count == 1:
            break
    
    subcontroller.demonstrate_capabilities(n_episodes=3)
    subcontroller.save("saved_controllers", "LOAD_SHELF_n_steps_ppo_new_reward")


    print("Training all the RL Subcontrollers")
    pass

def run_MCTS():
    '''
    Run the MCTS solution until something gets delivered
    '''
    print("Running the MCTS solution until something gets delivered")
    root_state = copy.deepcopy(glue_rl.get_current_state())
    root_node = node_rl.Node(root_state)
    root_node.visits = 1

    sol = MCTS(root_node)
    time = utils_rl.timer()
    sol.Run(MaxIteration, del_children=True, limit_del = True, clear_root=False)
    end_time = utils_rl.timer()
    print("Time taken: ", end_time - time)
    gameStates = sol.storeGameStates
    actions = sol.storeActions
    # print(gameStates)
    state_count = 0
    print("\n printing gameStates: \n")
    for state in gameStates:
        state_count += 1
        print("\n State: {}".format(state_count))
        for entity in state:
            print(entity)
    print("\n printing actions: \n")
    for action in actions:
        print(action)

    pass

if __name__ == "__main__":

    '''
    Flow:
    1. Train all the RL Subcontrollers
    2. Run the MCTS solution until something gets delivered
    3. Execute the RL subcontrollers as required by MCTS until you get a new request
    4. Repeat from step 2
    '''

    # TODO: Write loop to train all the RL Subcontrollers

# ----------------------------------------------------------------
    # Loop to run the MCTS solution
    train_rl_subcontrollers()
    # load_and_demonstrate("saved_controllers")
    # run_MCTS()
    # env.render()
    # time.sleep(5)

