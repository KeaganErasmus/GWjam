import pygame

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hover_color) -> None:
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input  = text_input
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image == None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))





    def update(self, surface):
        if self.image is not None:
            surface.blit(self.image, self.rect)
        
        surface.blit(self.text, self.text_rect)


    def check_input(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        
        return False
    
    def change_color(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)