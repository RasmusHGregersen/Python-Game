import pygame
from SnakeGame import SnakeGame
from q_table_template import q_table_template

pygame.init()
game=SnakeGame((720,720),True,1)
#window=pygame.display.set_mode(game.bounds)
pygame.display.set_caption("Snake")
game.main_game(3)