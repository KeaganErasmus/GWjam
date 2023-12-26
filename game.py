import sys, time

import pygame
from src.player import Player
from src.level import Level
from src.UI.button import Button

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Ninja runner")
    

        self.screen = pygame.display.set_mode((800, 480))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("./assets/background.png")

        self.font = self.get_font(30)
        self.old_time = time.time()

        self.score = 0
        self.scores = []

        self.mute = False

        self.level_1 = Level("level_1.tmx", self)
        self.level_1.load_level()
        self.level_1.create_level_rects()

        self.level_2 = Level("level_2.tmx", self)
        self.level_2.load_level()
        self.level_2.create_level_rects()

        self.level_3 = Level("level_3.tmx", self)
        self.level_3.load_level()
        self.level_3.create_level_rects()

        self.level_4 = Level("level_4.tmx", self)
        self.level_4.load_level()
        self.level_4.create_level_rects()

        self.level_5 = Level("level_5.tmx", self)
        self.level_5.load_level()
        self.level_5.create_level_rects()



        self.current_level = self.level_1
        self.movement = [False, False]

        self.player = Player(self, (0, 300))

    def get_font(self, size):
        return pygame.font.Font("assets/font.ttf", size)

    def draw_score(self):
        score_text = self.font.render(f'{self.score}', True, "black")
        self.screen.blit(score_text, (10, 10))

    def update_score(self):
        current_time = time.time()
        if current_time - self.old_time >= 1:
            self.score += 1
            self.old_time = current_time

    def run(self):
        pygame.mixer.music.load("./sounds/ambience.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        while True:
            self.screen.fill("white")
            self.screen.blit(pygame.transform.scale(self.background, self.screen.get_size()), (0, 0))

            if self.player.level_count == 0:
                self.level_1.draw_level()
            elif self.player.level_count == 1:
                self.current_level = self.level_2
                self.level_2.draw_level()
            elif self.player.level_count == 2:
                self.current_level = self.level_3
                self.level_3.draw_level()
            elif self.player.level_count == 3:
                self.current_level = self.level_4
                self.level_4.draw_level()
            elif self.player.level_count == 4:
                self.current_level = self.level_5
                self.level_5.draw_level()

            elif self.player.level_count == 5:
                self.player.level_count = 0
                self.current_level = self.level_1
                self.scores.append(self.score)
                self.finish_screen()

            self.draw_score()
            self.update_score()
            self.player.draw()
            self.player.update((self.movement[1] - self.movement[0], 0))

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player.direction = "left"
                        self.movement[0] = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player.direction = "right"
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE and self.player.is_jumping == False or event.key == pygame.K_UP and self.player.is_jumping == False or event.key == pygame.K_w and self.player.is_jumping == False:
                        self.player.jump()
                        self.player.is_jumping = True
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

                    if event.key == pygame.K_n :
                        self.player.debug_mode = True
                    if event.key == pygame.K_b:
                        self.player.debug_mode = False                        
                    if event.key == pygame.K_m:
                        self.mute = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            pygame.display.update()

            self.clock.tick(60)
    
    def main_menu(self):
        pygame.mixer.music.load("sounds/main_menu.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        self.scores.clear()
        self.score = 0

        while True:
            self.screen.fill("black")
            self.screen.blit(pygame.transform.scale(self.background, self.screen.get_size()), (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_input(MENU_MOUSE_POS):
                        # pygame.mixer.music.stop()
                        self.run()
                    if QUIT_BUTTON.check_input(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()


            MENU_TEXT = self.get_font(50).render("Bagio", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.screen.get_width()/2, 100))

            PLAY_BUTTON = Button(None, pos=(self.screen.get_width()/2, 250), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hover_color="White")

            QUIT_BUTTON = Button(None, pos=(self.screen.get_width()/2, 400), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hover_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(self.screen)

            pygame.display.update()

    def finish_screen(self):
        self.movement = [False, False]
        while True:
            self.screen.fill("black")
            self.screen.blit(pygame.transform.scale(self.background, self.screen.get_size()), (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_input(MENU_MOUSE_POS):
                        # pygame.mixer.music.stop()
                        self.main_menu()
                    if QUIT_BUTTON.check_input(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()


            MENU_TEXT = self.get_font(40).render(f"Your Score {self.scores}s", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.screen.get_width()/2, 50))

            THANKS_TEXT = self.get_font(30).render(f"Thank you for playing\n this small game", True, "#b68f40")
            THANKS_RECT = THANKS_TEXT.get_rect(center=(self.screen.get_width()/2, 150))

            PLAY_BUTTON = Button(None, pos=(self.screen.get_width()/2, 250), 
                                text_input="Menu", font=self.get_font(75), base_color="#d7fcd4", hover_color="White")

            QUIT_BUTTON = Button(None, pos=(self.screen.get_width()/2, 400), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hover_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            self.screen.blit(THANKS_TEXT, THANKS_RECT)

            for button in [PLAY_BUTTON ,QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(self.screen)

            pygame.display.update()


Game().main_menu()