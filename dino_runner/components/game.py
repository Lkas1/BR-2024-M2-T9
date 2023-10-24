import pygame
import os

from dino_runner.utils.constants import BG, MOON, CLOUD, CLOUD2, GROUND, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.utils.sound_constants import BG_MUSIC, MENU_MUSIC, GAMEOVER_MUSIC, BEEP
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.Text_types import draw_message_component
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 10
        self.x_pos_moon = 0
        self.y_pos_moon = 0
        self.x_pos_cloud = 0
        self.y_pos_cloud = 10
        self.x_pos_cloud2 = 0
        self.y_pos_cloud2 = 10
        self.x_pos_ground = 0
        self.y_pos_ground = 415
        self.score = 0
        self.death_count = 0

        self.bg_music = BG_MUSIC
        self.game_over_music = GAMEOVER_MUSIC
        self.menu_music = MENU_MUSIC
        self.beep = BEEP

        if os.path.exists('HighScore.txt'):
            with open('HighScore.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            self.high_score = 0

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

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
        self.game_over_music.stop()
        self.menu_music.stop()
        self.beep.play()
        pygame.time.delay(500)
        self.bg_music.play(loops = -1)
        self.bg_music.set_volume(0.5)
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.player.has_power_up = False
        self.score = 0
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.score > self.high_score:
                    self.high_score = self.score
                    with open('HighScore.txt', 'w') as file:
                        file.write(str(self.high_score))
                self.playing = False
                self.death_count +=1
                

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5
            if self.game_speed >= 50:
                self.game_speed = 50
        

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_moon()
        self.draw_cloud()
        self.draw_cloud2()
        self.draw_ground()
        self.draw_score()
        self.draw_high_score()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg + 150))
        self.screen.blit(BG, (image_width + self.x_pos_bg - 450, self.y_pos_bg + 150))
        self.screen.blit(BG, (image_width + self.x_pos_bg - 650, self.y_pos_bg + 150))
        if self.x_pos_bg >= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg + 1000, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_moon(self):
        image_width = MOON.get_width()
        self.screen.blit(MOON, (image_width + self.x_pos_moon, self.y_pos_moon))
        if self.x_pos_moon <= image_width:
            self.screen.blit(MOON, (image_width + self.x_pos_moon + 1000, self.y_pos_moon))
            self.x_pos_moon = 0
        self.x_pos_moon -= self.game_speed

    def draw_cloud(self):
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(CLOUD, (image_width + self.x_pos_cloud, self.y_pos_cloud))
        if self.x_pos_cloud >= -image_width:
            self.screen.blit(CLOUD, (image_width + self.x_pos_cloud - 1150, self.y_pos_cloud))
            self.x_pos_cloud = 0
        self.x_pos_cloud += self.game_speed

    def draw_cloud2(self):
        image_width = CLOUD2.get_width()
        self.screen.blit(CLOUD2, (self.x_pos_cloud2, self.y_pos_cloud2))
        self.screen.blit(CLOUD2, (image_width + self.x_pos_cloud2, self.y_pos_cloud2))
        if self.x_pos_cloud2 >= -image_width:
            self.screen.blit(CLOUD2, (image_width + self.x_pos_cloud2 - 1150, self.y_pos_cloud2))
            self.x_pos_cloud2 = 0
        self.x_pos_cloud2 += self.game_speed

    def draw_ground(self):
        image_width = GROUND.get_width()
        self.screen.blit(GROUND, (self.x_pos_ground, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 250, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 350, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 450, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 550, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 650, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 750, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 850, self.y_pos_ground))
        self.screen.blit(GROUND, (image_width + self.x_pos_ground + 950, self.y_pos_ground))
        if self.x_pos_ground <= -image_width:
            self.screen.blit(GROUND, (image_width + self.x_pos_ground, self.y_pos_ground))
            self.x_pos_ground = 0
        self.x_pos_ground -= self.game_speed

    def draw_score(self):
        draw_message_component(
            f"Score: {self.score}",
            self.screen,
            pos_x_center= 1000,
            pos_y_center= 50
        )
        
    def draw_high_score(self):
        draw_message_component(
            f"High Score: {self.high_score}",
            self.screen,
            font_color = ('purple2'),
            pos_x_center = 1000,
            pos_y_center = 25
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center= 50
                )  
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()   

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            image_width = BG.get_width()
            self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.screen.blit(BG, (image_width + self.x_pos_bg - 20, self.y_pos_bg + 150))
            self.screen.blit(BG, (image_width + self.x_pos_bg - 80, self.y_pos_bg + 150))
            self.screen.blit(BG, (image_width + self.x_pos_bg - 650, self.y_pos_bg + 150))
            self.screen.blit(BG, (image_width + self.x_pos_bg - 20, self.y_pos_bg + 300))
            self.screen.blit(BG, (image_width + self.x_pos_bg - 80, self.y_pos_bg + 300))
            self.screen.blit(BG, (image_width + self.x_pos_bg - 650, self.y_pos_bg + 300))
            self.menu_music.play()
            self.menu_music.set_volume(0.5)
            draw_message_component("Press any key to start", self.screen, font_color = ('purple3'))
        else: 
            self.bg_music.stop()
            self.menu_music.stop()
            self.game_over_music.play()
            self.game_over_music.set_volume(0.5)
            self.screen.fill('Red')
            draw_message_component("Press any key to restart", self.screen, font_color = ('black'), pos_y_center=half_screen_height + 140)
            draw_message_component( f"Your Score: {self.score}", self.screen, font_color = ('black'), pos_y_center=half_screen_height - 150)
            draw_message_component(f"Your high score: {self.high_score}", self.screen, font_color = ('black'), pos_y_center=half_screen_height - 125)
            draw_message_component( f"Death count: {self.death_count}", self.screen, font_color = ('black'), pos_y_center=half_screen_height - 100)
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 40))
            
            if self.score > self.high_score:
                self.high_score = self.score
                with open('HighScore.txt', 'w') as file:
                    file.write(str(self.high_score))


        pygame.display.update()

        self.handle_events_on_menu()
    
