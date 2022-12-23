#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
        s=self.pixel_size
        self.body=[(s,s),(2*s,s),(3*s,s)]
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
            return True
        return False
    
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

