import random
import json
import dataclasses
import pygame


@dataclasses.dataclass
class State_DataClass:
    distance: tuple
    position: tuple
    relative_state: str
    food: tuple


class Q_Learner(object): #from Learner
    

    def __init__(self, border_width, border_height, pixel_size):
        self.border_width = border_width
        self.border_height = border_height
        self.pixel_size = pixel_size
        self.epsilon = 0.1
        self.learning_rate = 0.5
        self.discount = .2
        self.q_table = self.Fetch_QValues()
        self.activity_log = []
        self.learner_directions_dict = {
            0:'LEFT',
            1:'RIGHT',
            2:'UP',
            3:'DOWN'
        }

        # Action space

    def Refresh_activity_log(self):
        self.activity_log = []
        
    def SaveRecord(self, path="q_table.json"):
        with open(path, "w") as f:
            json.dump(self.q_table, f)

    def Fetch_QValues(self, path="q_table.json"):
        with open(path, "r") as f:
            q_table = json.load(f)
        return q_table
            
    def choose_key(self, snake, food):
        state = self.FutureState(snake, food)

        # Epsilon greedy
        random_epsilon = random.uniform(0,1)
        if random_epsilon < self.epsilon:
            action_key = random.choices(list(self.learner_directions_dict.keys()))[0]
        else:
            state_scores = self.q_table[str((state.position[0],state.position[1],state.relative_state))]
            action_key = state_scores.index(max(state_scores))
        action_val = self.learner_directions_dict[action_key]
        
        # Remember the actions it took at each state
        self.activity_log.append({
            'state': state,
            'action': action_key
            })
        return action_val
    
    def UpdateQValues(self, reason):
        activity_log = self.activity_log[::-1]
        for state_number, state_data in enumerate(activity_log[:-1]):
            if reason: # Snake Died -> Negative reward
                stateN = activity_log[0]['state']
                actionN = activity_log[0]['action']
                state_str = str((stateN.position[0],stateN.position[1],stateN.relative_state))
                reward = -1
                self.q_table[state_str][actionN] = (1-self.learning_rate) * self.q_table[state_str][actionN] + self.learning_rate * reward # Bellman equation - there is no future state since game is over
                reason = None
            else:
                state1 = state_data['state'] # current state
                state0 = activity_log[state_number+1]['state'] # previous state
                action0 = activity_log[state_number+1]['action'] # action taken at previous state
                
                x1 = state0.distance[0] # x distance at current state
                y1 = state0.distance[1] # y distance at current state
    
                x2 = state1.distance[0] # x distance at previous state
                y2 = state1.distance[1] # y distance at previous state
                
                if state0.food != state1.food: # Snake ate a food, positive reward
                    reward = 1
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)): # Snake is closer to the food, positive reward
                    reward = 1
                else:
                    reward = -1 # Snake is further from the food, negative reward
                    
                state_str = str((state0.position[0],state0.position[1],state0.relative_state))
                new_state_str = str((state1.position[0],state1.position[1],state1.relative_state))
                self.q_table[state_str][action0] = (1-self.learning_rate) * (self.q_table[state_str][action0]) + self.learning_rate * (reward + self.discount*max(self.q_table[new_state_str])) # Bellman equation
        
    def distance_from_food(self,snake,food):
        
        snake_head = snake[-1]
        dist_x = food.x - snake_head[0]
        dist_y = food.y - snake_head[1]

        if dist_x > 0:
            pos_x = '1' # Food is to the right of the snake
        elif dist_x < 0:
            pos_x = '0' # Food is to the left of the snake
        else:
            pos_x = '-' # Food and snake are on the same X file

        if dist_y > 0:
            pos_y = '3' # Food is below snake
        elif dist_y < 0:
            pos_y = '2' # Food is above snake
        else:
            pos_y = '-' # Food and snake are on the same Y file
            
        return dist_x,dist_y,pos_x,pos_y

    def FutureState(self, snake, food):
        
        dist_x,dist_y,pos_x,pos_y= self.distance_from_food(snake,food)
        snake_head = snake[-1]
        possible_directions = [
            (snake_head[0]-self.pixel_size, snake_head[1]),   
            (snake_head[0]+self.pixel_size, snake_head[1]),         
            (snake_head[0],                  snake_head[1]-self.pixel_size),
            (snake_head[0],                  snake_head[1]+self.pixel_size),
        ]
        
        surrounding_list = []

        for direction in possible_directions:
            out_y=direction[1]>=self.border_width or direction[1]<0
            out_x=direction[0]>=self.border_height or direction[0]<0
            check_tail=direction in snake[:-1]
            
            if out_y==True: # off screen left or top
                surrounding_list.append('1')
            elif out_x==True: # off screen right or bottom
                surrounding_list.append('1')
            elif check_tail==True: # part of tail
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        relative_state = ''.join(surrounding_list)

        return State_DataClass((dist_x, dist_y), (pos_x, pos_y), relative_state, food)


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

class SnakeGame():
    bounds= None
    human_player = False
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
            
    def main_game(self,highest_score):
        

        #Size of snake links/food defined
        pixel_size=self.pixel_size
        
        death=None
        game_count=0


        #Snake made
        snake= Snake(pixel_size,self.bounds)
        learner=Q_Learner(self.bounds[0],self.bounds[1],pixel_size)

        #Food made

        food=Food(pixel_size,self.bounds)


        #Loop variable
        run=True


        timer=15000*(1/self.speed)
        time_back=timer

        while run:
                    
            if game_count>100:
                learner.epsilon=0 #reduce randomness
            else:
                learner.epsilon=0.1

            #Time delay for fps
            pygame.time.delay(int(100*(1/self.speed)))
            
            if self.human_player==True:
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
                key_dic={pygame.K_UP:"UP",pygame.K_DOWN:"DOWN",pygame.K_RIGHT:"RIGHT",pygame.K_LEFT:"LEFT"}
                action=learner.choose_key(snake.body,food)
                snake.control(action)

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
                death="True"
                if self.human_player==False:
                    snake.died()
                    food.eaten()
                    game_count+=1
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
            learner.UpdateQValues(death)
        
            Q_VALUES_N=100
            if game_count % Q_VALUES_N == 0:
                print(game_count)
            learner.SaveRecord()

        #Score and timer
            if snake.links>highest_score:
                highest_score=snake.links
                print(highest_score)

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
game=SnakeGame((720,720),True,10000)
window=pygame.display.set_mode(game.bounds)
pygame.display.set_caption("Snake")
#game.speed=2
game.main_game(3)