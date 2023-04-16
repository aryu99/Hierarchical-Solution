import time
import copy
import numpy as np

from low_level_controller.rl_controller import RLController
from low_level_controller.rl_utils import load_model

import utils_rl
from glue_rl import Glue
import node_rl
from config_rl import MAX_ITERATIONS_PER_ACTION, Actions, make_env
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
    TIMESTEPS =  2e2 # 3e6
    for action in Actions:
        count += 1
        print(action)
        subcontroller = RLController(action.value, action.value, training_mode=True, max_training_steps=MAX_TRAINING_STEPS, verbose=True)
        subcontroller.learn(total_timesteps=TIMESTEPS)
        # subcontroller.save("saved_controllers", str(action.name))
        # if count == 1:
        #     break
    
    # subcontroller.demonstrate_capabilities(n_episodes=3)
    # subcontroller.save("saved_controllers", "LOAD_SHELF_n_steps_ppo_new_reward")


    print("Training all the RL Subcontrollers")
    pass

def run_MCTS():
    '''
    Run the MCTS solution until something gets delivered
    '''
    print("Running the MCTS solution until something gets delivered")
    # abstract_sim = glue_rl.make_abstract_sim(env)
    global env
    global obs
    glue_object = Glue()
    env = glue_object.env
    obs = glue_object.obs
    root_state = copy.deepcopy(glue_object.get_current_state())
    root_node = node_rl.Node(root_state)
    root_node.visits = 1

    sol = MCTS(root_node, glue_object)
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

    return actions

if __name__ == "__main__":

    '''
    Flow:
    1. Train all the RL Subcontrollers
    2. Run the MCTS solution until something gets delivered
    3. Execute the RL subcontrollers as required by MCTS until you get a new request
    4. Repeat from step 2
    '''

    # TODO: Write loop to train all the RL Subcontrollers
    # train_rl_subcontrollers()

# ----------------------------------------------------------------
    # Loop to run the MCTS solution
    
    # load_and_demonstrate("saved_controllers")
    actions = run_MCTS()

    format_actions = utils_rl.format_actions(actions, env.shelfs)
    print(format_actions)

    # Demonstrate Actions
    env.training_mode = False

    idx = [0] * len(actions[0])
    break_flag = False
    while True:
        env.train_subcontroller = np.zeros(len(idx))
        counter = 0
        for id in idx:
            env.train_subcontroller[counter] = (actions[id][counter])
            counter += 1

        action_list = []
        while True:
            agent_id = 0
            for command in env.train_subcontroller:
                if len(command) == 1: # GOTO_GOAL
                    subcontroller = load_model("saved_controllers", "GOTO_GOAL", env=env)
                else:
                    if command[0] == 0: # LOAD_SHELF
                        subcontroller = load_model("saved_controllers", "LOAD_SHELF", env=env)
                    elif command[0] == 1: # UNLOAD_SHELF
                        subcontroller = load_model("saved_controllers", "UNLOAD_SHELF", env=env)
                    
                action, _states = subcontroller.predict(obs[agent_id], deterministic=True)
                action_list.append(action)
                agent_id += 1
            
            obs, rewards, dones, infos = env.step(action_list)

            if all(done == False for done in dones):
                continue

            elif all(dones):
                if all(x == len(actions) for x in idx):
                    print("All done")
                    break_flag = True

                idx = [x + 1 for x in idx]
            else:
                for done in range(dones):
                    if dones[done]:
                        idx[done] += 1
            break
        
        if break_flag:
            break
        else:
            continue

            

                



            
    # env.render()
    # time.sleep(5)

