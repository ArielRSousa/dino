from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle
import random

class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.image = [ self.image[0], self.image[1] ]
        self.rect.y = random.randint(200, 300)
        self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image[self.step_index // 5], self.rect)
        self.step_index += 1

        if self.step_index >= 9:
            self.step_index = 0
