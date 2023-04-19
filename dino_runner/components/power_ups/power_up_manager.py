import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.index = random.randint(0, 1)

    def generate_power_up(self, score, player):
        #power_up_list = [Hammer, Shield]
        if len(self.power_ups) == 0 and self.when_appears == score:
            if self.index == 0 and player.has_power_up == False:
                print(self.index )
                self.when_appears += random.randint(0, 300)
                self.power_ups.append(Shield())
            if self.index  == 1 and player.has_power_up == False:
                print(self.index)
                self.when_appears += random.randint(0, 300)
                self.power_ups.append(Hammer())
        

    def update(self, score, game_speed, player):
        self.generate_power_up(score,player)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect) and self.index == 0:
                print(self.index)
                power_up.start_time = pygame.time.get_ticks()
                player.shield = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = 0
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)
            elif player.dino_rect.colliderect(power_up.rect) and self.index  == 1:
                print(self.index)
                power_up.start_time = pygame.time.get_ticks()
                player.hammer = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = 0
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

            if player.hammer or player.shield == True:
                print('TRUE')    
               
           
              

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)                