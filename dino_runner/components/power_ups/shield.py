from dino_runner.utils.constants import SHIELD, SHIELD_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Shield(PowerUp): 
    def __init__(self, position):
        self.image = SHIELD
        self.type = SHIELD_TYPE
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        super().__init__(self.image, self.type)