#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
    

