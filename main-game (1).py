#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pygame
import random

#Snake class is defined
class Snake:
    
    #Possible directions of movement
    DIRECTIONS={"UP":(0,-1),"DOWN":(0,1),"LEFT":(-1,0),"RIGHT":(1,0)}
    
    #Lenght (sausage links haha) of snake and position of body 
    links=None
    body=None
    
    #Direction of snake
    direction=None
    
    #Size of snake parts
    pixel_size=None
    
    #Color of snake
    color=(0,0,255)
    borders=None
    
    #Iinitialize new snake
    def __init__(self, pixel_size, borders):
        self.pixel_size=pixel_size
        self.borders=borders
        self.died()
     
    #respawn function, three long
    def died(self):
        self.links=3
        self.body=[(20,20),(40,20),(60,20)]
        self.direction=self.DIRECTIONS["RIGHT"]
    
    #Move - next pixel in direction is made head, last pixel is removed
    def move(self):
        snake_head=self.body[-1]
        move=(self.direction[0]*self.pixel_size,self.direction[1]*self.pixel_size)
        new_head=(snake_head[0]+move[0],snake_head[1]+move[1])
        self.body.append(new_head)
        #If the snake has eaten food, tail is not popped
        if len(self.body)>self.links:
            self.body.pop(0)
    
    def control(self,direction):
        #If the direction is the same, or opposite no move
        if abs(self.direction[0])!=abs(self.DIRECTIONS[f'{direction}'][0]):
            self.direction=self.DIRECTIONS[f'{direction}']
    
    #Delicious!! - allows snake to grow longer
    def eat(self):
        self.links+=1
    
    #Yummy - checks if head is on food
    def found_food(self,food):
        mouth=self.body[-1]
        if mouth==(food.x,food.y):
            self.eat()
            food.eaten()
    
    #Checks for collision - if head is also present in rest of body, dead
    def check_tail(self):
        return self.body[-1] in self.body[:-1]
    
    #Checks for border - if head is not within, dead
    def check_border(self):
        head=self.body[-1]
        out_y=head[1]>=self.borders[1] or head[1]<0
        out_x=head[0]>=self.borders[0] or head[0]<0
        return out_y or out_x
    
    def animate(self,game,window):
        for segment in self.body:
            game.draw.rect(window, self.color, (segment[0],segment[1],self.pixel_size, self.pixel_size))
        
        #draw eyes - todo
        #maybe input head graphics - oriented by direction
        #game.draw.rect(window,(255,255,255),(self.body[-1][0]+5,self.body[-1][1]+5,4,4))

#Object class is defined

class Object:
    pixel_size = None
    color = (220,220,220)
    x = 0
    y = 0
    borders = None
    
    def __init__(self,pixel_size,borders):
        self.borders=borders
        self.pixel_size=pixel_size
    
    #
    def draw(self,game,window):
        game.draw.rect(window,self.color,(self.x,self.y,self.pixel_size,self.pixel_size))
    
class Food(Object):
    
    def __init__(self,pixel_size,borders):
        super().__init__(pixel_size,borders)
        self.color=(255,0,0)
        
    def eaten(self):
        x_pixels=(self.borders[0])/self.pixel_size
        y_pixels=(self.borders[1])/self.pixel_size
        self.x=random.randint(0,x_pixels-1)*self.pixel_size
        self.y=random.randint(0,y_pixels-1)*self.pixel_size
    
#Game initialised
pygame.init()
bounds=(600,600)
window=pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")

#Size of snake links/food defined
pixel_size=20

#Snake made
snake= Snake(pixel_size,bounds)

#Food made

food=Food(pixel_size,bounds)

#Font for game
game_over_font=pygame.font.SysFont(f'calibri',60,bold=True)
go_again_font=pygame.font.SysFont(f'cailibri',40,italic=True)


#Loop variable
run=True

while run:
    #Time delay for fps
    pygame.time.delay(100)
    
    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #If keydown - if keydown is a direction, snake is steered
        if event.type == pygame.KEYDOWN:
            key_dic={pygame.K_UP:"UP",pygame.K_DOWN:"DOWN",pygame.K_RIGHT:"RIGHT",pygame.K_LEFT:"LEFT"}
            if event.key in key_dic.keys():
                snake.control(key_dic[event.key])
    #Snake moves
    snake.move()
    
    #Checks for food
    snake.found_food(food)
    
    #Checks for death
    if snake.check_tail() or snake.check_border():
        
        #Game over printed
        game_over=game_over_font.render(f'Game over!',True,(255,0,0))
        game_over_rect = game_over.get_rect(center=(bounds[0]/2, bounds[1]/3))
        window.blit(game_over,game_over_rect)
        
        #Pres any key to play again
        go_again=go_again_font.render(f'Press any key to go again!',True,(255,0,0))
        go_again_rect=go_again.get_rect(center=(bounds[0]/2,bounds[1]*2/3))
        window.blit(go_again,go_again_rect)
        pygame.display.flip()
        
        wait=True
        while wait:
            #Checks for input
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    snake.died()
                    food.eaten()
                    wait=False
                if event.type==pygame.QUIT:
                    wait = False
                    run = False
                    
    window.fill((0,0,0))
    snake.animate(pygame,window)
    food.draw(pygame,window)
    pygame.display.flip()
pygame.quit()

