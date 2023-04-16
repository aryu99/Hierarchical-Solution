from stable_baselines3 import PPO
import os
import sys


def load_model(model_dir, model_name, load_env):
    """
    Load a model from a directory
    """

    path = os.path.join(model_dir, model_name)

    model = PPO.load(path, env=load_env)
    return model