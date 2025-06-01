import pygame
from settings import Colors

class Button:
    x_offset = 0
    y_offset = 60

    def __init__(self, x, y, width, height, text, font_size=48, color=Colors.BLUE.value):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(text, True, Colors.WHITE.value)
        self.bg_color = color
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(
            self.text_surface,
            (
                self.rect.centerx - self.text_surface.get_width() // 2,
                self.rect.centery - self.text_surface.get_height() // 2
            )
        )

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)