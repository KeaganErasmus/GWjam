import pygame
from pytmx.util_pygame import load_pygame

class Level:
    def __init__(self, level, game) -> None:
        pygame.init()
        self.level = level
        self.game = game
        self.layer = None
        self.walk = None
        self.level_finish = None
        self.tmx_data = None

        self.tile_size = 16
        self.tile_rects = []
        self.level_finish_rects = []

        self.debug_mode = False


    def load_level(self):
        self.tmx_data = load_pygame(f"./levels/{self.level}")
        self.layer = self.tmx_data.get_layer_by_name("ground_layer")
        self.walk = self.tmx_data.get_layer_by_name("walkable")
        try:
            self.level_finish  = self.tmx_data.get_layer_by_name("level_finish")
        except:
            pass

    def draw_level(self):
        try:
            for x, y, surface in self.level_finish.tiles():
                self.game.screen.blit(surface, ((x * self.tile_size), y * self.tile_size))
        except:
            pass

        for x, y, surface in self.walk.tiles():
            self.game.screen.blit(surface, ((x * self.tile_size), y * self.tile_size))

        for x, y, surface in self.layer.tiles():
            self.game.screen.blit(surface, ((x * self.tile_size), y * self.tile_size))


    def create_level_rects(self):
        for x, y, surface in self.walk.tiles():
            self.tile_rects.append(pygame.Rect((x * 16), (y * 16), self.tile_size, self.tile_size))
        
        try:
            for x, y, surface in self.level_finish.tiles():
                self.level_finish_rects.append(pygame.Rect((x * 16), (y * 16), self.tile_size, self.tile_size))
        except:
            pass
            
