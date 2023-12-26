import pygame, os


class Player:
    def __init__(self, game, pos) -> None:
        pygame.init()
        pygame.mixer.init()

        self.game    = game
        self.image   = pygame.image.load(os.path.join("./assets/player/", "bag.png"))
        self.width   = self.image.get_width() - 8.5
        self.height  = self.image.get_height()
        self.pos     = list(pos)
        self.level_count = 0

        self.level = self.game.current_level
        self.move_speed = 4.5
        self.velocity = [0, 0]
        self.jump_vel = 3.5
        self.jumps = 1

        self.direction = "right"
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.is_jumping = False
        self.on_wall = False

        self.debug_mode = False

        self.sfx = {
            'jump_2' : pygame.mixer.Sound("./sounds/jump_2.mp3"),
            'fall': pygame.mixer.Sound("./sounds/jump.mp3"),
            'level_finish': pygame.mixer.Sound("./sounds/level_finish.mp3"),
         }

        self.sfx['fall'].set_volume(0.1)
        self.sfx['level_finish'].set_volume(0.1)
        self.sfx['jump_2'].set_volume(0.5)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def update(self, movement=(0 ,0)):
        self.level = self.game.current_level
        # player_rect = self.rect()
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0] * self.move_speed

        self.check_collisions(frame_movement)
        self.velocity[1] = min(5, self.velocity[1] + 0.15)

        self.on_wall = False
        if (self.collisions['right'] or self.collisions['left']):
            self.jumps = 1
            self.on_wall = True
            
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.is_jumping = False
            self.jumps = 1

        if self.collisions['right'] or self.collisions['left']:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.is_jumping = False

        self.check_level_finish()
        self.check_bounds()

    def jump(self):
        if self.on_wall:
            if self.collisions['right']:
                self.velocity[1] = -self.jump_vel
                self.pos[0] -= 20
                self.jumps = max(0, self.jumps - 1)
            elif self.collisions['left']:
                self.velocity[1] = -self.jump_vel
                self.pos[0] += 20
        elif self.jumps:
            self.sfx['jump_2'].play()
            self.velocity[1] = -self.jump_vel
            self.jumps -= 1

    def check_collisions(self, frame_movement):
        # Horizontal Collisions
        player_rec = self.rect()
        for rect in self.level.tile_rects:
            if player_rec.colliderect(rect):
                if frame_movement[0] > 0:
                    player_rec.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    player_rec.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = player_rec.x

        # Veritcal collisions
        self.pos[1] += frame_movement[1]
        player_rec = self.rect()
        for rect in self.level.tile_rects:
            if player_rec.colliderect(rect):
                if frame_movement[1] > 0:
                    player_rec.bottom = rect.top
                    self.collisions['down'] = True

                if frame_movement[1] < 0:
                    player_rec.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = player_rec.y

    def check_level_finish(self):
        if self.rect().collidelistall(self.level.level_finish_rects):
            self.level_transistion()
                       
    def draw(self):
        if self.debug_mode:
            pygame.draw.rect(self.game.screen, "green", self.rect())
        # if self.direction == "left":
        #     self.game.screen.blit(pygame.transform.flip(self.image, True, False), self.pos)  
        # else:
        self.game.screen.blit(self.image, self.pos)

    def level_transistion(self):
        self.pos[0] = 0
        self.pos[1] = 300
        self.level_count += 1
        self.sfx['level_finish'].play()

    def check_bounds(self):
        if self.pos[1] >= self.game.screen.get_height():
            self.pos[1] = 300
            self.pos[0] = 0
            self.velocity[1] = 0
            self.sfx['fall'].play()
        
        if self.pos[0] <= 0:
            self.pos[0] = 0
        elif self.pos[0] >= self.game.screen.get_width() - self.width:
            self.pos[0] = self.game.screen.get_width() - self.width