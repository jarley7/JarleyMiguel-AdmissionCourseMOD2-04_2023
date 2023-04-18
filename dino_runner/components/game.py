import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obsatacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


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
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.start_screen = True
        self.last_score = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()



    def startScreen(self):
        if self.start_screen == True:
            self.clock.tick(FPS)
            self.screen.fill((255,255,255)) #Também aceita código hexadecimal "#FFFFFF"
            self.draw_background()
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
        self.player.update(user_input)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2
                
        


    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed


    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score:{self.score}", True, (0,0,0))
        text_rect = text.get_rect()
        text_score = (850, 30)
        self.screen.blit(text, text_score)

    def handle_events_on_menu(self):
        for event in pygame.event.get():
          if event.type == pygame.QUIT: 
           self.playing = False
           self.running = False
          elif event.type == pygame.KEYDOWN:
              self.run()      

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        if self.death_count == 0:
            self.startScreen()
            font = pygame.font.Font(FONT_STYLE, 22)
            text = font.render("Press any key to start", True,(0,0,0))
            self.screen.blit(text, (490,435))
        else:
            self.screen.blit(ICON,(595, 315))
            font = pygame.font.Font(FONT_STYLE, 22)
            death_text = font.render("You died, press any key to RESTART!", True,(0,0,0))
            self.screen.blit(death_text, (490,435))
            font = pygame.font.Font(FONT_STYLE, 22)
            last_score_text = font.render(f"Last score:{self.last_score}", True,(0,0,0))
            self.screen.blit(last_score_text, (850, 30))
            font = pygame.font.Font(FONT_STYLE, 22)
            death_count_text = font.render(f"{3 - self.death_count} attempts left.", True,(0,0,0))
            self.screen.blit(death_count_text, (490,500))
            
        pygame.display.update()
        self.handle_events_on_menu()