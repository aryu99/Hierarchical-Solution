from config_rl import Actions, sensor_range, n_requests, default_layout

from stable_baselines3 import PPO
from datetime import datetime
import pickle
import gym

import os
import sys
sys.path.append('../../robotic_warehouse/')

import rware

class RLController:
    '''
    RL Controller class that represents the RL Subcontroller
    for differen sub-tasks
    ''' 
    
    def __init__(self, controller_ind:int, controller_type:Actions.value, training_mode=False, max_training_steps=1e6, load_dir=None, verbose=False):
        '''
        Constructor for the RLController class
        
        Parameters
        ----------
        controller_ind : int
            The index of the controller
        target : tuple
            The target coordinates of the agent
        max_training_steps : int
            The maximum number of training steps for the RL controller
        env_settings : dict
            The environment settings
        verbose : bool
            The verbosity flag
        '''
        self.verbose = verbose

        self.controller_ind = controller_ind
        self.max_training_steps = max_training_steps
        self.controller_type = controller_type
        self.training_mode = training_mode


        self.data = {
            'total_training_steps' : 0,
            'performance_estimates' : {}
        }
        if load_dir is None:
            assert controller_ind is not None
            assert controller_type is not None
            self._set_training_env(training_mode)
            self._init_learning_alg()
        else:
            self.load(load_dir)
        
        self.init_model()


    def learn(self, total_timesteps=5e4):
        """
        Train the sub-system for a specified number of timesteps.

        Inputs
        ------
        total_timesteps : int
            Total number of timesteps to train the sub-system for.
        """
        self.model.learn(total_timesteps=total_timesteps)
        self.data['total_training_steps'] = self.data['total_training_steps'] + total_timesteps

    def predict(self, obs, deterministic=True):
        """
        Get the sub-system's action, given the current environment observation (state)

        Inputs
        ------
        obs : tuple
            Tuple representing the current environment observation (state).
        deterministic (optional) : bool
            Flag indicating whether or not to return a deterministic action or a distribution
            over actions.
        """
        action, _states = self.model.predict(obs, deterministic=deterministic)
        return action, _states
    
    def eval_performance(self, n_episodes=400, n_steps=100):
        """
        Perform empirical evaluation of the performance of the learned controller.

        Inputs
        ------
        n_episodes : int
            Number of episodes to rollout for evaluation.
        n_steps : int
            Length of each episode.
        """
        success_count = 0
        avg_num_steps = 0
        trials = 0
        total_steps = 0
        num_steps = 0

        rollout_successes = []

        for episode_ind in range(n_episodes):
            trials = trials + 1
            avg_num_steps = (avg_num_steps + num_steps) / 2

            obs = self.training_env.reset()
            num_steps = 0
            for step_ind in range(n_steps):
                num_steps = num_steps + 1
                total_steps = total_steps + 1
                action, _states = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.training_env.step(action)
                if step_ind == n_steps - 1:
                    rollout_successes.append(0)
                if done:
                    if info['task_complete']:
                        success_count = success_count + 1
                        rollout_successes.append(1)
                    else:
                        rollout_successes.append(0)
                    break

        # self.data['rollout_successes'][self.data['total_training_steps']] = rollout_successes
        self.data['performance_estimates'][self.data['total_training_steps']] = {
            'success_count' : success_count,
            'success_rate' : success_count / trials,
            'num_trials' : trials,
            'avg_num_steps' : avg_num_steps,
        }
    
    def save(self, save_dir):
        """
        Save the controller object.

        Inputs
        ------
        save_dir : string
            Absolute path to the directory that will be used to save this controller.
        """
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        model_file = os.path.join(save_dir, 'model')
        self.model.save(model_file)
        controller_file = os.path.join(save_dir, 'controller_data.p')

        controller_data = {
            'controller_ind' : self.controller_ind,
            'init_states' : self.init_states,
            'final_states' : self.final_states,
            'env_settings' : self.env_settings,
            'verbose' : self.verbose,
            'max_training_steps' : self.max_training_steps,
            'data' : self.data,
        }

        with open(controller_file, 'wb') as pickleFile:
            pickle.dump(controller_data, pickleFile)

    
    def load(self, save_dir):
        """
        Load a controller object

        Inputs
        ------
        save_dir : string
            Absolute path to the directory that will be used to save this controller.
        """

        controller_file = os.path.join(save_dir, 'controller_data.p')
        with open(controller_file, 'rb') as pickleFile:
            controller_data = pickle.load(pickleFile)

        self.controller_ind = controller_data['controller_ind']
        self.init_states = controller_data['init_states']
        self.final_states = controller_data['final_states']
        self.env_settings = controller_data['env_settings']
        self.max_training_steps = controller_data['max_training_steps']
        self.verbose = controller_data['verbose']
        self.data = controller_data['data']

        self._set_training_env(self.env_settings)

        model_file = os.path.join(save_dir, 'model')
        self.model = PPO.load(model_file, env=self.training_env)

    def _set_training_env(self, env_settings):
        self.training_env = gym.make("rware-tiny-2ag-v1", sensor_range=sensor_range, request_queue_size=n_requests, n_agents=1, layout=default_layout)
        self.training_env.agent_start_states = self.init_states
        self.training_env.goal_states = self.final_states


    def _init_learning_alg(self, verbose=False):
        self.model = PPO("MlpPolicy", 
                        self.training_env, 
                        verbose=verbose,
                        n_steps=512,
                        batch_size=64,
                        gae_lambda=0.95,
                        gamma=0.99,
                        n_epochs=10,
                        ent_coef=0.0,
                        learning_rate=2.5e-4,
                        clip_range=0.2)
    
    def demonstrate_capabilities(self, n_episodes=5, n_steps=100, render=True):
        """
        Demonstrate the capabilities of the learned controller in the environment used to train it.

        Inputs
        ------
        n_episodes : int
            Number of episodes to rollout for evaluation.
        n_steps : int
            Length of each episode.
        render (optional) : bool
            Whether or not to render the environment at every timestep.
        """
        for episode_ind in range(n_episodes):
            obs = self.training_env.reset()
            for step in range(n_steps):
                action, _states = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.training_env.step(action)
                if render:
                    self.training_env.render(highlight=False)
                if done:
                    break

        obs = self.training_env.reset()
