import json
import random
class Learner(Snake): #need to import the snake class
    def __init__(self, pixel_size,borders):
        super().__init__(pixel_size,borders)
        self.epsilon = 0.1
        self.learning_rate = 0.7
        self.discount = .5
        self.q_table=self.load_table()
        self.action_log=[] #make a dictionary of past actions to score 
    
    def load_table(self, path="qtable.json"): #load the q value template with all possible future states
        with open(path,"r") as table:
            q_table=json.load(table)
        return q_table
    
    def save_table(self,path="qtable.json"): #to save (not very necessary)
        with open (path,"w") as table:
            json.dump(self.q_table,table)
    
    def location_from_object(self,from_obj_x,from_obj_y): #food and snake location respective to each other
    
        if from_obj_x > 0:
            pos_x = '1' # Food is to the right of the snake
        elif from_obj_x < 0:
            pos_x = '0' # Food is to the left of the snake
        else:
            pos_x = '-' # Food and snake are on the same x value

        if from_obj_y > 0:
            pos_y = '3' # Food is below snake
        elif from_obj_y < 0:
            pos_y = '2' # Food is above snake
        else:
            pos_y = '-' # Food and snake are on the same y value
    
        return (pos_x,pos_y)
    
    def future_state(self,food): #document all future states, where food, where wall
        
        snake_head=self.body[-1]
        from_food_x= food[0]-snake_head[0] #x pos of snake head
        from_food_y= food[1]-snake_head[1] #y pos of snake head

        position_food= self.location_from_object(from_food_x,from_food_y)
        
        move=(self.direction[0]*self.pixel_size,self.direction[1]*self.pixel_size)
        
        head=self.body[-1]
        
        hit_bound=[]
        
        possible_directions=[(head[0]-move[0],head[1]),(head[0]+ move[0],head[1]),(head[0],head[1]-move[1]),(head[0],head[1]+move[1])]
        for direction in possible_directions:
            out_y=direction[1]>=self.borders[1] or direction[1]<0
            out_x=direction[0]>=self.borders[0] or direction[0]<0
            
            if out_y==True: #off the roof or floor
                hit_bound.append("1")
            elif out_x==True:#off the left bound or right bound
                hit_bound.append("1")
            elif direction in self.body[:-1]:#hit the tail
                hit_bound.append("1")
            else:
                hit_bound.append("0")
                
            bound = ''.join(hit_bound)
            
        return ((from_food_x, from_food_y), position_food, bound, food)
    
    def choose_key(self,food): #choose direction key randomly or based on the scores 
        
        future= self.future_state(food)
        rand= random.uniform(0,1)
        if rand < self.epsilon:
            chosen_key=random.choices(list(DIRECTIONS.keys()))[0] #Directions from snake class
        else:
            state_info=str((future[1][0],future[1][1],future[2])) #pos_x, pos_y,bound
            scores=self.qtable[state_info]
            chosen_key=scores.index(max(scores))
        chosen_value=DIRECTIONS["chosen_key"] #Directions from snake class
        
        self.history.append({
            'state': future,
            'action': chosen_key
            })
        
        return chosen_value
    
    def UpdateQ_table(self): #update the scores of each direction keys based on the results
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            if self.check_tail() or self.check_border(): # Snake Died -> Negative reward
                state_N = history[0]['state']
                action_N = history[0]['action']
                
                state_str = str((state_N[1][0],state_N[1][1],state_N[2]))
                
                reward = -1
                self.q_table[state_str][action_N] = (1-self.learning_rate) * self.q_table[state_str][action_N] + self.learning_rate * reward # Bellman equation 
                
            else:
                state_1 = h['state'] # current state
                state_0 = history[i+1]['state'] # previous state
                action_0 = history[i+1]['action'] # action taken at previous state
                
                
                x1 = state_0[0][0] # x distance at prev state
                y1 = state_0[0][1] # y distance at prev state
    
                x2 = state_1[0][0] # x distance at current state
                y2 = state_1[0][1] # y distance at current state
                
                if state_0[3] != state_1[3]: # Snake ate a food, positive reward
                    reward = 1
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)): # Snake is closer to the food, positive reward
                    reward = 1
                else:
                    reward = -1 # Snake is further from the food, negative reward
                    
                state_str = str((state_0[1][0],state_0[1][1],state_0[2]))
                new_state_str = str((state_1[1][0],state_1[1][1],state_1[2]))
                self.q_table[state_str][action_0] = (1-self.learning_rate) * (self.q_table[state_str][action_0]) + self.learning_rate * (reward + self.discount*max(self.q_table[new_state_str])) # Bellman equation