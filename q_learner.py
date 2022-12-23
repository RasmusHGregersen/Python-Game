from state_dataclass import State_DataClass
import json
import random

class Q_Learner(object): 

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
        chosen_key = self.learner_directions_dict[action_key]
        
        # Remember the actions it took at each state
        self.activity_log.append({
            'state': state,
            'action': action_key
            })
        return chosen_key
    
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
                
                current_x = state0.distance[0] # x distance at current state
                current_y = state0.distance[1] # y distance at current state
    
                previous_x = state1.distance[0] # x distance at previous state
                previous_y = state1.distance[1] # y distance at previous state
                
                if state0.food != state1.food: # Snake ate a food, positive reward
                    reward = 1
                elif (abs(current_x) > abs(previous_x) or abs(current_y) > abs(previous_y)): # Snake is closer to the food, positive reward
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

        #relative position of the food to the snake
        if dist_x > 0:
            pos_x = '1' # right of the snake
        elif dist_x < 0:
            pos_x = '0' # left of the snake
        else:
            pos_x = '-' # on the same X

        if dist_y > 0:
            pos_y = '3' # below snake
        elif dist_y < 0:
            pos_y = '2' # above snake
        else:
            pos_y = '-' # on the same Y
            
        return dist_x,dist_y,pos_x,pos_y

    def FutureState(self, snake, food):
        
        dist_x,dist_y,pos_x,pos_y= self.distance_from_food(snake,food)
        snake_head = snake[-1]
        possible_directions = [
            (snake_head[0]-self.pixel_size, snake_head[1]),   
            (snake_head[0]+self.pixel_size, snake_head[1]),         
            (snake_head[0],snake_head[1]-self.pixel_size),
            (snake_head[0],snake_head[1]+self.pixel_size),
        ]
        
        surrounding_list = []

        for direction in possible_directions:
            out_y=direction[1]>=self.border_width or direction[1]<0
            out_x=direction[0]>=self.border_height or direction[0]<0
            check_tail=direction in snake[:-1]
            
            if out_y==True:
                surrounding_list.append('1')
            elif out_x==True: 
                surrounding_list.append('1')
            elif check_tail==True: 
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        relative_state = ''.join(surrounding_list)

        return State_DataClass((dist_x, dist_y), (pos_x, pos_y), relative_state, food)