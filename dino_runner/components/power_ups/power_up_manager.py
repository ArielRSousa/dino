import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import POINT_SOUND

point_sound = pygame.mixer.Sound(POINT_SOUND)

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.next_power_up_time = 0

    def generate_power_up(self, score): # faz o power up aparecer
        if len(self.power_ups) == 0 and self.when_appears <= score:
            if pygame.time.get_ticks() > self.next_power_up_time:
                self.when_appears = score
                x_pos = random.randint(900, 1100)
                y_pos = random.randint(200, 300)
                if random.choice([True, False]):
                    self.power_ups.append(Shield((x_pos, y_pos)))
                else:
                    self.power_ups.append(Hammer((x_pos, y_pos)))
                self.next_power_up_time = pygame.time.get_ticks() + random.randint(10, 15000) # faz o power up aparecer em um tempo aleatorio
    
    def update(self, game): 
        self.generate_power_up(game.score) 
        for power_up in self.power_ups: 
            power_up.update(game.game_speed, self.power_ups) 
            if game.player.dino_rect.colliderect(power_up.rect):
                if isinstance(power_up, Hammer):
                    game.score += 100  # Adicione essa linha para aumentar o score ao colidir com o martelo
                    point_sound.play()
                else:
                    point_sound.play()
                power_up.start_time = pygame.time.get_ticks()
                game.player.shield = True
                game.player.hammer = True
                game.player.has_power_up = True
                game.player.type = power_up.type
                game.player.power_up_time = power_up.start_time + (power_up.duration * 500)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups: 
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(300, 500) #faz o power up aparecer em um tempo aleatorio inicialmente
        self.next_power_up_time = 0