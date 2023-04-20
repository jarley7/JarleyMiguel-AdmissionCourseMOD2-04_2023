import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
    def __init__(self):
        self.position = random.randint(0,1)
        self.step_index = 0
        super().__init__(BIRD, self.position)
        if self.position == 0:
            self.rect.y = 255
        else:
            self.rect.y = 325

    def draw(self, screen):
        image = self.image[0] if self.step_index < 5 else self.image[1]
        screen.blit(image, (self.rect.x, self.rect.y))

        if self.step_index >= 10:
            self.step_index = 0
        self.step_index += 1