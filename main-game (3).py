#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import random


#Taken from stack overflow
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('calibri', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

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

        
def game(bounds,human_player=True,timed=False,speed=1):  
    #Game initialised
    pygame.init()
    window=pygame.display.set_mode(bounds)
    pygame.display.set_caption("Snake")

    #Size of snake links/food defined
    pixel_size=40
    

    #Snake made
    snake= Snake(pixel_size,bounds)

    #Food made

    food=Food(pixel_size,bounds)

    #Font for game
    game_over_font=pygame.font.SysFont(f'calibri',bounds[1]//10,bold=True)
    small_font=pygame.font.SysFont(f'calibri',bounds[1]*2//30,italic=True)



    #Loop variable
    run=True
    
        
    timer=15000*(1/speed)
    time_back=timer
    
    while run:
        
        #Time delay for fps
        pygame.time.delay(int(100*(1/speed)))
        
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
        if snake.found_food(food):
            snake.found_food(food)
            timer=time_back
        else:
            if timed:
                timer-=100*(1/speed)
            

        #Checks for death
        if snake.check_tail() or snake.check_border() or timer==0:
            timer=time_back
            if not human_player:
                snake.died()
                food.eaten()
            else:
                #Game over printed
                game_over=game_over_font.render(f'Game over!',True,(255,0,0))
                game_over_rect = game_over.get_rect(center=(bounds[0]/2, bounds[1]/3))
                window.blit(game_over,game_over_rect)

                #Pres any key to play again
                go_again=small_font.render(f'Press any key to go again!',True,(255,0,0))
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
        
        #Background color - filled with black
        window.fill((0,0,0))

        #Snake is drawn
        snake.animate(pygame,window)
        food.draw(pygame,window)

        #Score and timer

        score=small_font.render(f'Score: {snake.links}',True,(255,0,0))
        score_rect=score.get_rect(center=(bounds[0]*3/20,bounds[1]/20))
        window.blit(score,score_rect)
        
        if timed:
            time=small_font.render(f'{int(timer//1000)}:{int((timer%1000)/10)}',True,(255,0,0))
            time_rect=time.get_rect(center=(bounds[0]*(18/20),bounds[1]/20))
            window.blit(time,time_rect)
        pygame.display.flip()
    pygame.quit()
    return snake.links


class SnakeGame():
    bounds= None
    human_player = True
    timed= False
    speed= None
    pixel_size=20
    game_over_font=None
    small_font=None

    def __init__(self,bounds,timed,speed):
        self.bounds=bounds
        self.timed=timed
        self.speed=speed
        self.game_over_font=pygame.font.SysFont(f'calibri',self.bounds[1]//10,bold=True)
        self.small_font=pygame.font.SysFont(f'calibri',self.bounds[1]*2//30,italic=True)
    def menu(self):
        while True:
            welcome_text=self.game_over_font.render(f'Snake: Main Menu',True, (255,255,255))
            welcome_rect=welcome_text.get_rect(center=(self.bounds[0]//2,self.bounds[1]/3))
            window.blit(welcome_text,welcome_rect)
            new_game=button("grey",self.bounds[0]//2,self.bounds[0]*2/3,self.pixel_size*6,self.pixel_size*2,f'New Game')
            #Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
    def main_game(self):
        

        #Size of snake links/food defined
        pixel_size=self.pixel_size


        #Snake made
        snake= Snake(pixel_size,self.bounds)

        #Food made

        food=Food(pixel_size,self.bounds)


        #Loop variable
        run=True


        timer=15000*(1/self.speed)
        time_back=timer

        while run:

            #Time delay for fps
            pygame.time.delay(int(100*(1/self.speed)))
            
            if self.human_player:
                #Event handler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    #If keydown - if keydown is a direction, snake is steered
                    if event.type == pygame.KEYDOWN:
                        key_dic={pygame.K_UP:"UP",pygame.K_DOWN:"DOWN",pygame.K_RIGHT:"RIGHT",pygame.K_LEFT:"LEFT"}
                        if event.key in key_dic.keys():
                            snake.control(key_dic[event.key])
            else:
                snake.control(key_dic[model.choose_key(food)])


            #Snake moves
            snake.move()

            #Checks for food
            if snake.found_food(food):
                snake.found_food(food)
                timer=time_back
            else:
                if self.timed:
                    timer-=100*(1/self.speed)


            #Checks for death
            if snake.check_tail() or snake.check_border() or timer==0:
                timer=time_back
                if not self.human_player:
                    snake.died()
                    food.eaten()
                else:
                    #Game over printed
                    game_over=self.game_over_font.render(f'Game over!',True,(255,0,0))
                    game_over_rect = game_over.get_rect(center=(self.bounds[0]/2, self.bounds[1]/3))
                    window.blit(game_over,game_over_rect)

                    #Pres any key to play again
                    go_again=self.small_font.render(f'Press any key to go again!',True,(255,0,0))
                    go_again_rect=go_again.get_rect(center=(self.bounds[0]/2,self.bounds[1]*2/3))
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
                                pygame.quit()

            #Background color - filled with black
            window.fill((0,0,0))

            #Snake is drawn
            snake.animate(pygame,window)
            food.draw(pygame,window)

            #Score and timer

            score=self.small_font.render(f'Score: {snake.links}',True,(255,0,0))
            score_rect=score.get_rect(center=(self.bounds[0]*3/20,self.bounds[1]/20))
            window.blit(score,score_rect)

            if self.timed:
                time=self.small_font.render(f'{int(timer//1000)}:{int((timer%1000)/10)}',True,(255,0,0))
                time_rect=time.get_rect(center=(self.bounds[0]*(18/20),self.bounds[1]/20))
                window.blit(time,time_rect)
            pygame.display.flip()
        return snake.links
#Game initialised
pygame.init()
game=SnakeGame((720,720),True,1)
window=pygame.display.set_mode(game.bounds)
pygame.display.set_caption("Snake")
#game.speed=2
game.main_game()


# In[ ]:




