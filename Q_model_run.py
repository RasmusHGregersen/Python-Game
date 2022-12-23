import pygame
from SnakeGame import SnakeGame
from Q_Learn_SnakeGame import Q_Learn_SnakeGame
from q_table_template import q_table_template
q_table_template()

pygame.init()
episodes=200 #the number of episodes
game=Q_Learn_SnakeGame((720,720),True,10000,episodes)
#window=pygame.display.set_mode(game.bounds)
pygame.display.set_caption("Snake")
game.q_learn_main_game()