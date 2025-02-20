import pygame
from gym_game.envs.SnakeGame import SnakeGame
from gym_game.envs.Snake import Snake
from gym_game.envs.q_learner import Q_Learner
from gym_game.envs.Food import Food
import matplotlib.pyplot as plt
import pandas as pd
from csv import writer
import os

class Q_Learn_SnakeGame(SnakeGame):
    # Constants for epsilon decay (exploration rate)
    INITIAL_EPSILON = 0.1
    MIN_EPSILON = 0.005
    EPSILON_DECAY_RATE = 0.99  # Exponential decay factor per episode

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
        train_df["Total_Score"] = pd.to_numeric(train_df["Total_Score"], errors='coerce').fillna(0)
        train_df["Highest_Score"] = pd.to_numeric(train_df["Highest_Score"], errors='coerce').fillna(0)

        # Extract columns as lists
        game_range = train_df["Range"].tolist()
        total_score = train_df["Total_Score"].tolist()
        highest_score = train_df["Highest_Score"].tolist()

        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, sharey=False, figsize=(8, 10))

        # --- Plot total scores ---
        ax1.bar(game_range, total_score, width=2)
        ax1.set_title("Total Scores in each 50-game Range")
        ax1.set_xlabel("50-game Ranges")
        ax1.set_ylabel("Total Score")
        ax1.set_ylim([0, max(total_score) + 5])
        
        # --- Plot highest scores ---
        ax2.bar(game_range, highest_score, width=2)
        ax2.set_title("Highest Scores in each 50-game Range")
        ax2.set_xlabel("50-game Ranges")
        ax2.set_ylabel("Highest Score")
        ax2.set_ylim([0, max(highest_score) + 5])
        
        # Limit the number of x-ticks to 20 at most.
        import numpy as np
        if len(game_range) > 20:
            indices = np.linspace(0, len(game_range) - 1, 20, dtype=int)
            tick_positions = [game_range[i] for i in indices]
            ax1.set_xticks(tick_positions)
            ax2.set_xticks(tick_positions)
        else:
            ax1.set_xticks(game_range)
            ax2.set_xticks(game_range)

        # Save the figure
        fig.tight_layout()
        fig.savefig("Train_Information.png")



    def q_learn_main_game(self):
        # Define the CSV filename
        csv_filename = "train.csv"
        
        # If the file exists, remove it so we start fresh.
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
        
        # Write the header once at the start
        self.game_record(["Range", "Total_Score", "Highest_Score"], filename=csv_filename)
        
        # Then proceed with training...
        window = pygame.display.set_mode(self.bounds)
        clock = pygame.time.Clock()
        snake = Snake(self.pixel_size, self.bounds)
        learner = Q_Learner(self.bounds[0], self.bounds[1], self.pixel_size)
        food = Food(self.pixel_size, self.bounds)

        game_count = 0
        total_game_score = 0
        highest_score = self.highest_score
        TIMER_START = 15000 * (1 / self.speed)
        timer = TIMER_START
        time_back = timer

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
                timer = time_back
                total_game_score += snake.links
                snake.died()
                food.eaten(snake)
                game_count += 1
                # After game_count += 1:
                if learner.epsilon > learner.epsilon_min:
                    learner.epsilon *= learner.epsilon_decay

                # Record performance data every 50 episodes
                if game_count % 20 == 0:
                    self.game_record([game_count, total_game_score, highest_score], filename=csv_filename)
                    total_game_score = 0
                    highest_score = 3

                if game_count < self.episodes - 2:
                    window.fill((0, 0, 0))
                    progress_text = self.small_font.render(f'Game: {game_count}/{self.episodes}', True, (255, 255, 255))
                    progress_rect = progress_text.get_rect(bottomright=(self.bounds[0] - 10, self.bounds[1] - 10))
                    window.blit(progress_text, progress_rect)
                    pygame.display.flip()
                    pygame.time.delay(50)
                    snake = Snake(self.pixel_size, self.bounds)
                    continue

            learner.UpdateQValues(False)

            if game_count % 20 == 0:
                learner.Refresh_activity_log()
                learner.SaveRecord()

            if snake.links > highest_score:
                highest_score = snake.links

            if game_count >= self.episodes - 2 or game_count%50 == 0:
                window.fill((0, 0, 0))
                snake.animate(pygame, window)
                food.draw(pygame, window)
                score = self.small_font.render(f'Score: {snake.links}', True, (255, 0, 0))
                score_rect = score.get_rect(center=(self.bounds[0] * 3 / 20, self.bounds[1] / 20))
                window.blit(score, score_rect)
                if self.timed:
                    time_text = self.small_font.render(f'{int(timer // 1000)}:{int((timer % 1000) / 10)}', True, (255, 0, 0))
                    time_rect = time_text.get_rect(center=(self.bounds[0] * (18 / 20), self.bounds[1] / 20))
                    window.blit(time_text, time_rect)
                game_text = self.small_font.render(f'Game: {game_count}/{self.episodes}', True, (255, 255, 255))
                game_text_rect = game_text.get_rect(bottomright=(self.bounds[0] - 10, self.bounds[1] - 10))
                window.blit(game_text, game_text_rect)
                pygame.display.flip()
                clock.tick(60)

            if game_count > self.episodes:
                break

        pygame.quit()
        self.plot_scores(filename=csv_filename)
        return snake.links

    def game_record(self, data, filename="train.csv"):
        with open(filename, 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
