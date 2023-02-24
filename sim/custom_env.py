# TODO : Deprecate this file

import sys
sys.path.append('../../robotic_warehouse/')

import time

import rware
from rware.warehouse import ObserationType
import gym


class custom_env():

    # default_layout = """
    # .........
    # .X.....X.
    # .........
    # ....X....
    # .........
    # .........
    # .........
    # ...ggg...
    # """

    default_layout = """
    X....
    .....
    ..g..
    """
    

    def __init__(self, sensor_range=9, request_queue_size=1, layout=default_layout, n_agents=2, observation_type=ObserationType.FLATTENED):
        self.layout = layout
        self.sensor_range = sensor_range
        self.request_queue_size = request_queue_size
        self.n_agents = n_agents
        self.observation_type = observation_type
        self.env = self.make()

    def make(self):
        return gym.make("rware-tiny-2ag-v1", sensor_range=self.sensor_range, request_queue_size=self.request_queue_size, n_agents=self.n_agents, layout=self.layout, observation_type=self.observation_type)

    def reset(self):
        return self.env.reset()

    def render(self):
        return self.env.render()
        
    def step(self,action):
        return self.env.step(action)

    def get_action_space(self):
        return self.env.action_space

    def get_observation_space(self):
        return self.env.observation_space

    def get_request_queue(self):
        return self.env.request_queue

    def close(self):
        return self.env.close()


