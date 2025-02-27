import pygame
from gym_game.envs.SnakeGame import SnakeGame
from gym_game.envs.Snake import Snake
from gym_game.envs.q_learner import Q_Learner
from gym_game.envs.Food import Food
import matplotlib.pyplot as plt
import pandas as pd
from csv import writer
import os
import numpy as np
import imageio

class Q_Learn_SnakeGame(SnakeGame):
    # Constants for epsilon decay (exploration rate)
    INITIAL_EPSILON = 0.1
    MIN_EPSILON = 0.005
    EPSILON_DECAY_RATE = 0.999  # Exponential decay factor per episode

    def __init__(self, bounds, timed, speed, episodes=100):
        super().__init__(bounds, timed, speed)
        self.highest_score = 3  # default starting highest score
        self.episodes = episodes

    def game_record(self, data, filename="train.csv"):
        # Append a row of data to the CSV file
        with open(filename, 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)

    def plot_scores(self, filename="train.csv"):
        # Read the CSV
        train_df = pd.read_csv(filename)

        # Sort the data by "Range" so bars appear in ascending order of episode range
        train_df = train_df.sort_values(by="Range", ascending=True)

        # Convert score columns to numeric values (if they're not already)
        train_df["Total_Score"] = pd.to_numeric(train_df["Total_Score"], errors='coerce').fillna(0).div(50)
        train_df["Highest_Score"] = pd.to_numeric(train_df["Highest_Score"], errors='coerce').fillna(0)
        train_df["Tail_Death"] = pd.to_numeric(train_df["Tail_Death"], errors='coerce').fillna(0)
        train_df["Border_Death"] = pd.to_numeric(train_df["Border_Death"], errors='coerce').fillna(0)
        train_df["Time_Death"] = pd.to_numeric(train_df["Time_Death"], errors='coerce').fillna(0)

        # Extract columns as lists
        game_range = train_df["Range"].tolist()
        total_score = train_df["Total_Score"].tolist()
        highest_score = train_df["Highest_Score"].tolist()
        tail_deaths = train_df["Tail_Death"].tolist()
        border_deaths = train_df["Border_Death"].tolist()
        time_deaths = train_df["Time_Death"].tolist()

        # Create a figure with two subplots:
        # 1. Scores (total and highest) as bar charts.
        # 2. Death types as line plots.
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 12))

        # --- Plot total and highest scores on ax1 ---
        ax1.plot(game_range, total_score, marker = "o", label="Average Score")
        ax1.plot(game_range, highest_score, marker = "o", label="Highest Score")
        ax1.set_title("Scores in each 50-game Range")
        ax1.set_ylabel("Score")
        ax1.legend()
        ax1.set_ylim([0, max(total_score + highest_score) + 5])
        
        # --- Plot death types on ax2 ---
        ax2.plot(game_range, tail_deaths, marker='o', label="Tail Deaths")
        ax2.plot(game_range, border_deaths, marker='o', label="Border Deaths")
        ax2.plot(game_range, time_deaths, marker='o', label="Time Deaths")
        ax2.set_title("Death Types Over Training")
        ax2.set_xlabel("50-game Ranges")
        ax2.set_ylabel("Death Count")
        ax2.legend()

        # Limit x-ticks to at most 20 for clarity.
        if len(game_range) > 20:
            indices = np.linspace(0, len(game_range) - 1, 20, dtype=int)
            tick_positions = [game_range[i] for i in indices]
            ax2.set_xticks(tick_positions)
        else:
            ax2.set_xticks(game_range)

        fig.tight_layout()
        fig.savefig("Train_Information.png")



    def q_learn_main_game(self):
        # Define the CSV filename
        csv_filename = "train.csv"
        
        # If the file exists, remove it so we start fresh.
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
        
        # Write the header once at the start (including death types)
        self.game_record(["Range", "Total_Score", "Highest_Score", "Tail_Death", "Border_Death", "Time_Death"], filename=csv_filename)
        
        # Then proceed with training...
        window = pygame.display.set_mode(self.bounds)
        clock = pygame.time.Clock()
        snake = Snake(self.pixel_size, self.bounds)
        learner = Q_Learner(self.bounds[0], self.bounds[1], self.pixel_size)
        food = Food(self.pixel_size, self.bounds)

        game_count = 0
        total_game_score = 0
        highest_score = self.highest_score
        TIMER_START = 7000 * (1 / self.speed)
        timer = TIMER_START
        time_back = timer
        tail_death = 0
        border_death = 0
        time_death = 0
        frames = []  # to store frames for the GIF
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return snake.links

            # Update epsilon, simulation steps, etc.
            if game_count > 0:
                learner.epsilon = max(self.MIN_EPSILON, self.INITIAL_EPSILON * (self.EPSILON_DECAY_RATE ** game_count))
            else:
                learner.epsilon = self.INITIAL_EPSILON

            action = learner.choose_key(snake.body, food)
            snake.control(action)
            snake.move()

            if snake.found_food(food):
                snake.found_food(food)
                timer = time_back
            else:
                if self.timed:
                    timer -= 100 * (1 / self.speed)

            if snake.check_tail() or snake.check_border() or timer <= 0:
                if snake.check_tail():
                    tail_death +=1
                if snake.check_border():
                    border_death +=1
                if timer <= 0:
                    time_death += 1

                timer = time_back
                total_game_score += snake.links
                snake.died()
                food.eaten(snake)
                game_count += 1
                # After game_count += 1:
                if learner.epsilon > learner.epsilon_min:
                    learner.epsilon *= learner.epsilon_decay

                # Record performance data every 50 episodes
                if game_count % 50 == 0:
                    self.game_record([game_count, total_game_score, highest_score, tail_death, border_death, time_death], filename=csv_filename)
                    total_game_score = 0
                    highest_score = 3
                    tail_death = 0
                    border_death = 0
                    time_death = 0
                learner.UpdateQValues(True)
                if game_count < self.episodes - 1:
                    window.fill((0, 0, 0))
                    progress_text = self.small_font.render(f'Game: {game_count}/{self.episodes}', True, (255, 255, 255))
                    progress_rect = progress_text.get_rect(bottomright=(self.bounds[0] - 10, self.bounds[1] - 10))
                    window.blit(progress_text, progress_rect)
                    pygame.display.flip()
                    pygame.time.delay(50)
                    snake = Snake(self.pixel_size, self.bounds)
                    continue
            else:
                learner.UpdateQValues(False)

            if game_count % 50 == 0:
                learner.Refresh_activity_log()
                learner.SaveRecord()

            if snake.links > highest_score:
                highest_score = snake.links

            if game_count >= self.episodes - 2 or game_count%20 == 0:
                window.fill((0, 0, 0))
                snake.animate(pygame, window)
                food.draw(pygame, window)
                score = self.small_font.render(f'Score: {snake.links}', True, (255, 0, 0))
                score_rect = score.get_rect(center=(self.bounds[0] * 3 / 20, self.bounds[1] / 20))
                window.blit(score, score_rect)
                #if self.timed:
                    #time_text = self.small_font.render(f'{int(timer // 1000)}:{int((timer % 1000) / 10)}', True, (255, 0, 0))
                    #time_rect = time_text.get_rect(center=(self.bounds[0] * (18 / 20), self.bounds[1] / 20))
                    #window.blit(time_text, time_rect)
                game_text = self.small_font.render(f'Game: {game_count}/{self.episodes}', True, (255, 255, 255))
                game_text_rect = game_text.get_rect(bottomright=(self.bounds[0] - 10, self.bounds[1] - 10))
                window.blit(game_text, game_text_rect)
                if game_count == self.episodes or game_count == 0:
                    frame_data = pygame.surfarray.array3d(window)
                    # Pygame surfaces are (width, height), but imageio expects (height, width)
                    frame_data = np.transpose(frame_data, (1, 0, 2))
                    frames.append(frame_data)
                pygame.display.flip()
                clock.tick(30)

            if game_count > self.episodes:
                break

        pygame.quit()
        # Save frames as a GIF
        imageio.mimsave("trained_demo.gif", frames, fps=15)
        print(f"Demo saved!")
        self.plot_scores(filename=csv_filename)
        return snake.links
    
    def demo_game(self, demo_episodes=1, out_gif="demo.gif"):
        """
        Demonstrate the trained Q-Learner with epsilon=0 (pure exploitation).
        Captures frames and saves them as a GIF.
        """
        # Create a new window (or reuse if you like)
        window = pygame.display.set_mode(self.bounds)
        clock = pygame.time.Clock()

        # Create a new snake, food, and Q-learner
        snake = Snake(self.pixel_size, self.bounds)
        food = Food(self.pixel_size, self.bounds)
        learner = Q_Learner(self.bounds[0], self.bounds[1], self.pixel_size)
        
        # Force the Q-Learner to load from disk (where you saved it after training)
        learner.q_table = learner.Fetch_QValues("q_table.json")

        # Epsilon = 0 => always exploit
        learner.epsilon = 0.0

        frames = []  # to store frames for the GIF

        episode_count = 0
        done = False

        while episode_count < demo_episodes:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Agent picks the best action from Q-table
            action = learner.choose_key(snake.body, food)
            snake.control(action)
            snake.move()

            # Check if the snake ate food
            snake.found_food(food)  # extends length if true

            # Check death
            if snake.check_tail() or snake.check_border():
                # End of an episode
                snake.died()
                food.eaten(snake)
                episode_count += 1
                if episode_count < demo_episodes:
                    # Reset for next demo episode
                    snake = Snake(self.pixel_size, self.bounds)
                    food = Food(self.pixel_size, self.bounds)
                    continue
                else:
                    done = True

            # Render the game
            window.fill((0, 0, 0))
            snake.animate(pygame, window)
            food.draw(pygame, window)
            pygame.display.flip()

            # Capture frame
            frame_data = pygame.surfarray.array3d(window)
            # Pygame surfaces are (width, height), but imageio expects (height, width)
            frame_data = np.transpose(frame_data, (1, 0, 2))
            frames.append(frame_data)

            clock.tick(15)  # 15 FPS for the demo (adjust as you like)

            if done:
                break

        pygame.quit()

        # Save frames as a GIF
        imageio.mimsave(out_gif, frames, fps=15)
        print(f"Demo saved to {out_gif}!")

    def game_record(self, data, filename="train.csv"):
        with open(filename, 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
