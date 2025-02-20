import pygame
from gym_game.envs.q_learner import Q_Learner
from gym_game.envs.Button import button
from gym_game.envs.Snake import Snake
from gym_game.envs.Food import Food

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
    def first_menu(self):
        welcome_font=pygame.font.SysFont(f'Corbel',self.bounds[1]//14,bold=True)
        window=pygame.display.set_mode(self.bounds)
        run=True
        while run:
            #Background color - filled with black
            window.fill((0,0,0))
            #Welcome text and buttons for exit game and new game made
            welcome=welcome_font.render(f'Welcome to Snake game',True,(255,0,0))
            welcome_rect=welcome.get_rect(center=(self.bounds[0]/2,self.bounds[1]/5))
            window.blit(welcome,welcome_rect)
            new_game_button=button((220,220,220),self.bounds[0]/4,self.bounds[1]/3,self.bounds[0]/2,self.bounds[1]/4,'New game')
            new_game_button.draw(window)
            exit_button = button((220,220,220),self.bounds[0]/4,self.bounds[1]*2/3,self.bounds[0]/2,self.bounds[1]/4,'Exit game')
            exit_button.draw(window)
            pygame.display.flip()
            #Controls whether buttons have been pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if exit_button.isOver(pos):
                        run=False
                    elif new_game_button.isOver(pos):
                        self.game_menu()
                        run=False
        pygame.quit()
    def game_menu(self):
        info_text=pygame.font.SysFont(f'Corbel',self.bounds[1]*2//30,bold=True)
        window=pygame.display.set_mode(self.bounds)
        run = True
        while run:
            
            window.fill((0,0,0))
            #Buttons for selecting difficulty
            difficulty=info_text.render(f'Difficulty {self.speed}',True,(255,0,0))
            dif_rect=difficulty.get_rect(center=(self.bounds[0]/2,self.bounds[1]/5))
            window.blit(difficulty,dif_rect)
            b_1=button((220,220,220),self.bounds[0]/6,self.bounds[1]/4,self.bounds[0]/6,self.bounds[1]/6,f'Dif 1')
            b_1.draw(window)
            b_2=button((220,220,220),self.bounds[0]/2-self.bounds[0]/12,self.bounds[1]/4,self.bounds[0]/6,self.bounds[1]/6,f'Dif 2')
            b_2.draw(window)
            b_3=button((220,220,220),self.bounds[0]*4/6,self.bounds[1]/4,self.bounds[0]/6,self.bounds[1]/6,f'Dif 3')
            b_3.draw(window)
            
            #Button for selecting timed or not
            t="Timed" if self.timed else "Not Timed"
            time=info_text.render(f'{t}',True,(255,0,0))
            time_rect=time.get_rect(center=(self.bounds[0]/2,self.bounds[1]*5/10))
            window.blit(time,time_rect)
            
            yes_button=button((220,220,220),self.bounds[0]/6,self.bounds[1]*11/20,self.bounds[0]/4,self.bounds[1]/6,'Timed') 
            yes_button.draw(window)
            no_button=button((220,220,220),self.bounds[0]*58/100,self.bounds[1]*11/20,self.bounds[0]/4,self.bounds[1]/6,'Not') 
            no_button.draw(window)
            
            start=button((50,205,50),self.bounds[0]/6,self.bounds[1]*9/12,self.bounds[0]*2/3,self.bounds[1]/6,'Start Game')
            start.draw(window)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if b_1.isOver(pos):
                        self.speed=1
                    elif b_2.isOver(pos):
                        self.speed=2
                    elif b_3.isOver(pos):
                        self.speed=3
                    elif yes_button.isOver(pos):
                        self.timed=True
                    elif no_button.isOver(pos):
                        self.timed=False
                    elif start.isOver(pos):
                        self.main_game()
                        run=False
        pygame.quit()

    def main_game(self):
        

        #Size of snake links/food defined
        pixel_size=self.pixel_size
        window=pygame.display.set_mode(self.bounds)
        game_over_font=pygame.font.SysFont(f'Corbel',self.bounds[1]//10,bold=True)
        small_font=pygame.font.SysFont(f'Corbel',self.bounds[1]*2//30,italic=True)
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
            #Time delay for fps
            pygame.time.delay(int(50*(1/self.speed)))

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

                #Press to try again or go back to main menu
                again_button=button((220,220,220),self.bounds[0]/4,self.bounds[1]/3,self.bounds[0]/2,self.bounds[1]/4,'Go again')
                again_button.draw(window)
                back_button = button((220,220,220),self.bounds[0]/4,self.bounds[1]*2/3,self.bounds[0]/2,self.bounds[1]/4,'Back to menu')
                back_button.draw(window)
                pygame.display.flip()
                wait=True
                while wait:
                    #Checks for input
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            if back_button.isOver(pos):
                                run=False
                                wait=False
                                self.first_menu()
                            elif again_button.isOver(pos):
                                wait=False
                                snake.died()
                                food.eaten(snake)
                        if event.type==pygame.QUIT:
                            wait=False
                            run = False
           
        pygame.quit()
        return snake.links
