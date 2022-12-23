import pygame
from SnakeGame import SnakeGame
from Snake import Snake
from q_learner import Q_Learner
from Food import Food
import matplotlib.pyplot as plt
import pandas as pd
from csv import writer

class Q_Learn_SnakeGame(SnakeGame): 
    def __init__(self,bounds, timed, speed,episodes):
        super().__init__(bounds, timed, speed)
        self.episodes=episodes
        self.highest_score=3 #default
    
    def game_record(self,data,filename="train.csv"): #Record Total Scores and Highest Score per 50 episodes throughout the game

        with open(filename, 'a') as f_object:
     
            writer_object = writer(f_object)

            writer_object.writerow(data)

            f_object.close()
    
    def plot_scores(self,filename="train.csv"): #Plot the scores and save the png as Train_Information

        train_df=pd.read_csv(filename)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharey=False,figsize=(8,10))

        game_range = list(train_df["Range"])
        highest_score = list(train_df["Highest_Score"])
        total_score = list(train_df["Total_Score"])

        ax1.bar(game_range, total_score)
        ax1.set_title("Total Scores in each episodes")
        ax1.set_xticks(game_range)
        ax1.set_xlabel("50-game Episodes")
        ax1.set_ylabel("Total Score")
        ax2.bar(game_range, highest_score)
        ax2.set_xticks(game_range)
        ax2.set_title("HIghest Scores in each episodes")
        ax2.set_xlabel("50-game Episodes")
        ax2.set_ylabel("Highest Score")

        fig.savefig("Train_Information.png")

            
    def q_learn_main_game(self):

        #Size of snake links/food defined
        pixel_size=self.pixel_size
        window=pygame.display.set_mode(self.bounds)
        
        #learner variables
        game_count=0
        death=None
        total_game_score=0
        highest_score=self.highest_score

        #Snake made
        snake= Snake(pixel_size,self.bounds)
        #Learner made
        learner=Q_Learner(self.bounds[0],self.bounds[1],pixel_size)

        #Create Columns in the record file
        self.game_record(["Range","Total_Score","Highest_Score"])

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
            
            if game_count>self.episodes: #End the training after the desired number of games is reached and plot the scores
                    run = False
                    self.plot_scores()
            else: #choose a move to make
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
            if snake.check_tail() or snake.check_border() or timer<=0:
                timer=time_back
                death="True"
                total_game_score+=snake.links
                snake.died()
                food.eaten(snake)
                game_count+=1
                #Save information for every 50-game
                if game_count % 50==0:
                    game_record=[game_count,total_game_score,highest_score]
                    self.game_record(game_record)
                    total_game_score=0 #Reset total game scores
                    highest_score=3 #Reset highest score

            #Background color - filled with black
            window.fill((0,0,0))

            #Snake is drawn
            snake.animate(pygame,window)
            food.draw(pygame,window)
            learner.UpdateQValues(death)

            if game_count % 50 == 0: #Save Q Values and Refresh Activity Log
                #print(game_count)
                learner.Refresh_activity_log()
                learner.SaveRecord()

            #Score and timer
            if snake.links>highest_score: #Check Highest Score
                highest_score=snake.links
                #print(highest_score)

            score=self.small_font.render(f'Score: {snake.links}',True,(255,0,0))
            score_rect=score.get_rect(center=(self.bounds[0]*3/20,self.bounds[1]/20))
            window.blit(score,score_rect)

            if self.timed:
                time=self.small_font.render(f'{int(timer//1000)}:{int((timer%1000)/10)}',True,(255,0,0))
                time_rect=time.get_rect(center=(self.bounds[0]*(18/20),self.bounds[1]/20))
                window.blit(time,time_rect)

            pygame.display.flip()
        pygame.quit()
        return snake.links