#!/usr/bin/env python
# coding: utf-8

# In[4]:


import random 
import Snake 

class Food():
    pixel_size = None
    color = (255,0,0)
    x = 0
    y = 0
    borders = None
    def __init__(self,pixel_size,borders):
        self.pixel_size=pixel_size
        self.border=borders
        
    def eaten(self):
        x_pixels=(self.borders[0])/self.pixel_size
        y_pixels=(self.borders[1])/self.pixel_size
        self.x=random.randint(0,x_pixels-1)*self.pixel_size
        self.y=random.randint(0,y_pixels-1)*self.pixel_size
        while (self.x,self.y) in snake.body:
            self.x=random.randint(0,x_pixels-1)*self.pixel_size
            self.y=random.randint(0,y_pixels-1)*self.pixel_size
        
    def draw(self,game,window):
        game.draw.rect(window,self.color,(self.x,self.y,self.pixel_size,self.pixel_size))
    

