import numpy as np
import gym
import pygame
from gym_game.envs.q_table_template import q_table_template
import argparse

parser = argparse.ArgumentParser('My program')

parser.add_argument('-m', '--mode',choices=["AI","human"],required=True)
parser.add_argument('-s', '--speed',type=int,default=1)
parser.add_argument('-me', '--max_episodes',type=int,default=100)
args = parser.parse_args()


def simulate():
    q_table_template()
    pygame.init()
    env.reset()
    env.render(mode,bounds,timed,speed,max_episodes)

if __name__ == "__main__":
    mode= args.mode
    bounds= (720,720)
    speed= args.speed
    timed=True
    max_episodes=args.max_episodes
    env = gym.make("Pygame-v0",disable_env_checker=True)
    pygame.init()
    simulate()
