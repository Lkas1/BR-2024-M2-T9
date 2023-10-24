import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

bird_height  = [320, 240]

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.rect.y = random.choice(bird_height)
        self.index = 0

    def draw(self, screen):
        if self.index >= len(BIRD):
            self.index = 0
        screen.blit(self.image[self.index], self.rect)
        self.index += 1