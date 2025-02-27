import random
from gym_game.envs.game_objects import Object

class Food(Object):
    
    def __init__(self,pixel_size,borders):
        super().__init__(pixel_size,borders)
        self.color=(255,0,0)
        
    def eaten(self,snake):
        x_pixels=(self.borders[0])/self.pixel_size
        y_pixels=(self.borders[1])/self.pixel_size
        self.x=random.randint(3,x_pixels-3)*self.pixel_size
        self.y=random.randint(3,y_pixels-3)*self.pixel_size
        while (self.x,self.y) in snake.body:
            self.x=random.randint(3,x_pixels-3)*self.pixel_size
            self.y=random.randint(3,y_pixels-3)*self.pixel_size