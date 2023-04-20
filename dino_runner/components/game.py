import pygame
import random

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obsatacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, CLOUD, GAMEOVER, DEAD
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.text_utils import draw_message_component

FONT_STYLE = "freesansbold.ttf"
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.new_game_speed = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = 0
        self.y_pos_cloud = 20
        self.obstacles_beaten = 0
        self.score = 0
        self.start_screen = True
        self.last_score = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()



    def startScreen(self):
        if self.start_screen == True:
            self.clock.tick(FPS)
            self.screen.fill((255,255,255)) #Também aceita código hexadecimal "#FFFFFF"
            self.draw_background()
            self.draw_clouds()
            self.player.runLoop()
            self.player.draw(self.screen)
        elif pygame.key.get_pressed():
            self.start_screen = False  
            return   

    
    def execute(self):
        self.running = True
        while not self.playing:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()
            
    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.score,self.player)
        while self.playing:
            self.events()
            self.update()
            self.draw()           

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.obstacle_manager.update(self)
        user_input = pygame.key.get_pressed()

        if user_input[pygame.K_2]:
            self.game_speed += 100
        if user_input[pygame.K_3]:
            self.game_speed = 20        
        self.player.update(user_input)
        self.update_score()
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 1000 == 0:
            self.game_speed += 0
                
        


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.draw_clouds()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time(self)
        self.death()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def death(self):
       if self.playing == False:
        self.player.dead(self.playing,self.screen)   
        self.screen.blit(GAMEOVER,(440, 170))
        pygame.time.delay(2000)    

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
        

        user_input = pygame.key.get_pressed() #Volta no tempo (se bugar apagar isso aq)
        if user_input[pygame.K_5]:
            self.game_speed -= 100

  
    def draw_clouds(self):
        bg_image_width = BG.get_width()
        image_width = CLOUD.get_width()
        value_clouds = random.randint(3,7)
        random_cloud_y = random.randint(20,150)
        random_cloud_x = random.randint(10,50)
        self.x_pos_cloud -= self.game_speed
    
        
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud - 43, self.y_pos_cloud + 20))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud - 78 , self.y_pos_cloud+ 45))
        self.screen.blit(CLOUD, (image_width  + self.x_pos_cloud - 200, self.y_pos_cloud + 50))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud + 80, self.y_pos_cloud + 20))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud + 145 , self.y_pos_cloud+ 40))
        self.screen.blit(CLOUD, (image_width  + self.x_pos_cloud + 200, self.y_pos_cloud + 35))
        if self.x_pos_cloud <= -bg_image_width:
            self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
            self.x_pos_cloud = 1300
        



    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score:{self.score}", True, (0,0,0))
        text_rect = text.get_rect()
        text_score = (850, 30)
        self.screen.blit(text, text_score)

    def draw_power_up_time(self, player):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.",
                    self.screen,
                    font_size = 18,
                    pos_x_center   = 500,
                    pos_y_center = 40
                )
            else:
                self.player.has_power_up = False
                self.player.hammer = False
                self.player.shield = False
                self.player.type = DEFAULT_TYPE
                self.power_up_manager.reset_power_ups(self.score, self.player)
                


    def handle_events_on_menu(self):
        for event in pygame.event.get():
          if event.type == pygame.QUIT: 
           self.playing = False
           self.running = False
          elif event.type == pygame.KEYDOWN:
              self.obstacles_beaten = 0 
              self.run()      

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        if self.death_count == 0:
            self.startScreen()
            font = pygame.font.Font(FONT_STYLE, 22)
            text = font.render("Press any key", True,(0,0,0))
            self.screen.blit(text, (490,350))
        else:
            self.screen.blit(GAMEOVER,(440, 170))
            pygame.time.delay(1000)
            self.screen.blit(ICON,(595, 315))
            font = pygame.font.Font(FONT_STYLE, 22)
            death_text = font.render("Press any key to RESTART!", True,(0,0,0))
            self.screen.blit(death_text, (490,435))
            font = pygame.font.Font(FONT_STYLE, 22)
            last_score_text = font.render(f"Last score:{self.last_score}", True,(0,0,0))
            self.screen.blit(last_score_text, (560, 250))
            font = pygame.font.Font(FONT_STYLE, 22)
            death_count_text = font.render(f"Death counts: {self.death_count}", True,(0,0,0))
            self.screen.blit(death_count_text, (540,470))
            beaten = font.render(f"Obstacles beaten whit hammer: {self.obstacles_beaten}", True,(0,0,0))
            self.screen.blit(beaten, (450,500))
            
        pygame.display.update()
        self.handle_events_on_menu()