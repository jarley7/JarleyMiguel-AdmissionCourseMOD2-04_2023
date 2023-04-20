import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        index = random.randint(0,2)
        obstacle_list = [SMALL_CACTUS, LARGE_CACTUS, BIRD]
        if len(self.obstacles) == 0:
            if index == 0 or index == 1:
                self.obstacles.append(Cactus(obstacle_list[index]))
            else:
                self.obstacles.append(Bird())            
                

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    game.last_score = game.score
                    game.score = game.score - game.score
                    game.game_speed = 20
                    break
                if game.player.has_power_up: self.obstacles.remove(obstacle)
                if game.player.hammer == True and game.player.dino_rect.colliderect(obstacle.rect):
                    game.obstacles_beaten = game.obstacles_beaten + 1
                    game.score += (game.obstacles_beaten * 10) #multiplica a quantidade de obstaculos por 10 e soma ao score
                    print(game.obstacles_beaten)
                    print(game.score)
                   
        

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []        