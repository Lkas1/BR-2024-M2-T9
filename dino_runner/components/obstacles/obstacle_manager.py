import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import HAMMER_TYPE, HOURGLASS_TYPE

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        obstacle_type = [
            Cactus(),
            Bird(),
        ]
        if len(self.obstacles) == 0:
            self.obstacles.append(obstacle_type[random.randint(0, 1)])

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.has_power_up and game.player.type == HAMMER_TYPE:
                    self.obstacles.remove(obstacle)
                elif game.player.has_power_up and game.player.type == HOURGLASS_TYPE:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break     
                else:
                    game.playing = True

    def reset_obstacles(self):
        self.obstacles = []

    def draw (self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)