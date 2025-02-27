import json
import random
import os
from gym_game.envs.state_dataclass import State_DataClass

class Q_Learner(object):
    def __init__(self, border_width, border_height, pixel_size):
        self.border_width = border_width
        self.border_height = border_height
        self.pixel_size = pixel_size

        # -- Hyperparameters --
        self.learning_rate = 0.1      # Lowered from 0.5
        self.discount = 0.9           # Values future rewards more
        self.epsilon = 1.0            # Start fully exploring
        self.epsilon_decay = 0.9995    # Exponential decay rate per episode
        self.epsilon_min = 0.01       # Minimum epsilon

        # Load or initialize Q-table
        self.q_table = self.Fetch_QValues()
        self.activity_log = []
        self.learner_directions_dict = {
            0: 'LEFT',
            1: 'RIGHT',
            2: 'UP',
            3: 'DOWN'
        }
        # Default Q-values if a state key is missing
        self.default_q_values = [0.0, 0.0, 0.0, 0.0]

    def Refresh_activity_log(self):
        self.activity_log = []

    def SaveRecord(self, path="q_table.json"):
        with open(path, "w") as f:
            json.dump(self.q_table, f)

    def Fetch_QValues(self, path="q_table.json"):
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    q_table = json.load(f)
                except json.JSONDecodeError:
                    q_table = {}
        else:
            q_table = {}
        return q_table

    def get_state_key(self, state):
        # Create a consistent string key including distance to food info and wall distance.
        # Here, state.position is (dist_x, dist_y), and we now include state.wall_distance.
        return str((state.position[0], state.position[1], state.relative_state))

    def ensure_state_in_qtable(self, state):
        key = self.get_state_key(state)
        if key not in self.q_table:
            self.q_table[key] = self.default_q_values.copy()
        return key

    def choose_key(self, snake, food):
        """Select an action via epsilon-greedy."""
        state = self.FutureState(snake, food)
        key = self.ensure_state_in_qtable(state)

        if random.random() < self.epsilon:
            # Explore
            action_key = random.choice(list(self.learner_directions_dict.keys()))
        else:
            # Exploit
            state_scores = self.q_table[key]
            action_key = state_scores.index(max(state_scores))

        chosen_key = self.learner_directions_dict[action_key]
        self.activity_log.append({'state': state, 'action': action_key})
        return chosen_key

    def UpdateQValues(self, reason):
        """
        reason = True if the snake died at the last move, else None/False.
        """
        # Reverse the log so we can do backward updates
        activity_log = self.activity_log[::-1]

        for i in range(len(activity_log) - 1):
            # If the snake just died in the last step
            if i == 0 and reason:
                terminal_state = activity_log[0]['state']
                action_terminal = activity_log[0]['action']
                key_term = self.ensure_state_in_qtable(terminal_state)

                # Heavier penalty for death
                reward = -3
                old_value = self.q_table[key_term][action_terminal]
                self.q_table[key_term][action_terminal] = (
                    (1 - self.learning_rate) * old_value
                    + self.learning_rate * reward
                )
                continue
            else:
                # Standard transition from state0 -> state1
                state1 = activity_log[i]['state']       # next state
                action0 = activity_log[i+1]['action']     # action from previous state
                state0 = activity_log[i+1]['state']       # previous state

                key0 = self.ensure_state_in_qtable(state0)
                key1 = self.ensure_state_in_qtable(state1)

                # Compute reward:
                reward = 0
                # If the snake ate the food
                if state0.food != state1.food:
                    reward += 1.0

                # Manhattan distance to food
                prev_dist = abs(state0.distance[0]) + abs(state0.distance[1])
                curr_dist = abs(state1.distance[0]) + abs(state1.distance[1])

                # If we moved closer to the food, add some reward
                if curr_dist < prev_dist:
                    reward += 0.5
                else:
                    # If we moved further, small penalty
                    reward -= 0.5

                old_value = self.q_table[key0][action0]
                next_max = max(self.q_table[key1])  # best action in next state
                new_value = (1 - self.learning_rate) * old_value + \
                            self.learning_rate * (reward + self.discount * next_max)
                self.q_table[key0][action0] = new_value

    def distance_from_food(self, snake, food):
        snake_head = snake[-1]
        dist_x = food.x - snake_head[0]
        dist_y = food.y - snake_head[1]

        # Relative horizontal position
        if dist_x > 0:
            pos_x = '1'
        elif dist_x < 0:
            pos_x = '0'
        else:
            pos_x = '-'

        # Relative vertical position
        if dist_y > 0:
            pos_y = '0'
        elif dist_y < 0:
            pos_y = '1'
        else:
            pos_y = '-'
        return dist_x, dist_y, pos_x, pos_y

    def FutureState(self, snake, food):
        """
        Create a state representation that includes:
         - The distance (dist_x, dist_y) from the snake head to the food.
         - A positional indicator (pos_x, pos_y) for the food relative to the snake.
         - A 4-character string (relative_state) indicating obstacles around the snake.
         - The food object (for detection of eating).
        """
        dist_x, dist_y, pos_x, pos_y = self.distance_from_food(snake, food)
        snake_head = snake[-1]
        possible_directions = [
            (snake_head[0] - self.pixel_size, snake_head[1]),
            (snake_head[0] + self.pixel_size, snake_head[1]),
            (snake_head[0], snake_head[1] - self.pixel_size),
            (snake_head[0], snake_head[1] + self.pixel_size),
        ]

        surrounding_list = []
        for direction in possible_directions:
            out_y = direction[1] >= self.border_width or direction[1] < 0
            out_x = direction[0] >= self.border_height or direction[0] < 0
            check_tail = direction in snake[:-1]
            if out_y or out_x or check_tail:
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')

        relative_state = ''.join(surrounding_list)
        return State_DataClass((dist_x, dist_y), (pos_x, pos_y), relative_state, food)
