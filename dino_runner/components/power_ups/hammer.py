from dino_runner.utils.constants import HAMMER, HAMMER_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Hammer(PowerUp): #Herencia da clase PowerUp
    def __init__(self, position):
        self.image = HAMMER
        self.type = HAMMER_TYPE
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        super().__init__(self.image, self.type)