import pygame
from random import randint
from time import sleep
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, RESET_BUTTON, CLOUD
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import GAMEROVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component

FONT_STYLE = "freesansbold.ttf"
TEXT_COLOR_BLACK = (0, 0, 0)

class Cloud():
    def __init__(self):
        self.x = SCREEN_WIDTH + randint(800, 1000)
        self.game_speed = 20 
        self.y = randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width() # Largura da imagem

    def update(self):
        self.x -= self.game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + randint(800, 1000)
            self.y = randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

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
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.high_score = 0
        self.clouds = []

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.game_speed = 20
        self.saved_score = self.score
        self.score = 0 
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
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
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        if randint(0, 1000) < 3:
            self.clouds.append(Cloud())
        for cloud in self.clouds:
            cloud.update()
        self.power_up_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score  # Atualizar o high score
        if self.score % 100 == 0:
            self.game_speed += 2

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))  # '#FFFFFF'
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_score()
        self.draw_high_score()
        self.draw_power_up_time()
        for cloud in self.clouds:
            cloud.draw(self.screen)
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
        draw_message_component(
            f"Score: {self.score}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=50,
        )
    def draw_high_score(self):
        draw_message_component(
            f"High Score: {self.high_score}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=80,
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 1)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    self.screen,
                    font_size=18,
                    pos_x_center=500,
                    pos_y_center=40
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:  # Tela de inicio
            draw_message_component("Press any key to start", self.screen,)
        else:  
            self.screen.blit(GAMEROVER, (half_screen_width - 180, half_screen_height - 60))
            self.screen.blit(RESET_BUTTON, (half_screen_width -40 , half_screen_height + 80))
            draw_message_component(
                f"High Score: {self.high_score}",
                self.screen, pos_y_center=half_screen_height + 1
            )
            draw_message_component(
                f"Your Score: {self.score}",
                self.screen, pos_y_center=half_screen_height + 30
            )
            draw_message_component(
                f"Death Count: {self.death_count}",
                self.screen, pos_y_center=half_screen_height + 60
            )
            draw_message_component(
                "Press any key to restart", self.screen, pos_y_center=half_screen_height + 160
            )

        pygame.display.update() 
        self.handle_events_on_menu()

    def handle_events_on_menu(self): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()