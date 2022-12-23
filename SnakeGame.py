import pygame
from q_learner import Q_Learner
from Button import button
from Snake import Snake
from Food import Food

class SnakeGame():
    bounds= None
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
            window=pygame.display.set_mode(self.bounds)
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
        window=pygame.display.set_mode(self.bounds)
        
        #learner variables
        game_count=0
        death=None

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

            #Time delay for fps
            pygame.time.delay(int(100*(1/self.speed)))

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
                if self.timed:
                    timer-=100*(1/self.speed)


            #Checks for death
            if snake.check_tail() or snake.check_border() or timer==0:
                timer=time_back
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
                            food.eaten(snake)
                            wait=False
                        if event.type==pygame.QUIT:
                            run = False
                            wait = False

            #Background color - filled with black
            window.fill((0,0,0))

            #Snake is drawn
            snake.animate(pygame,window)
            food.draw(pygame,window)

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