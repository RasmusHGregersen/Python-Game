from gym_game.envs.custom_env import *
from gym_game.envs.SnakeGame import SnakeGame
from gym_game.envs.Q_Learn_SnakeGame import Q_Learn_SnakeGame

from gym.envs.registration import register
register(
    id="Pygame-v0",
    entry_point="gym_game.envs.custom_env:SnakeEnv",  # Or wherever your Env class lives
)