import gym
from gym import spaces
import numpy as np
import pygame
from gym_game.envs.Q_Learn_SnakeGame import Q_Learn_SnakeGame
from gym_game.envs.q_learner import Q_Learner
from gym_game.envs.SnakeGame import SnakeGame
from gym_game.envs.q_table_template import q_table_template

class SnakeEnv(gym.Env):
    metadata = {'render.modes' : ['human','AI']}
    def __init__(self):

        pygame.init()
        #self.bounds=bounds
        #self.timed=timed
        #self.speed=speed
        #self.max_episodes=max_episodes
        #self.q_game=Q_Learn_SnakeGame(bounds,timed,speed,max_episodes)
        #self.human_game=SnakeGame(bounds,timed,speed)
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([10, 10, 10, 10, 10]), dtype=np.int)

    def reset(self):
        pass

    def step(self, action):
        pass

    def render(self, mode,bounds,timed,speed,max_episodes, close=False):
        if mode=="human":
            #self.human_game=SnakeGame(bounds,timed,speed)
            SnakeGame(bounds,timed,speed).first_menu()
        else:
            #self.q_game=Q_Learn_SnakeGame(bounds,timed,speed,max_episodes)
            Q_Learn_SnakeGame(bounds,timed,speed,max_episodes).q_learn_main_game()

