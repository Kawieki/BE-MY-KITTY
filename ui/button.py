import pygame
from settings import Colors

class Button:
    x_offset = 0
    y_offset = 60

    def __init__(self, x, y, width, height, label, font=None, font_size=48, color=Colors.BLUE.value):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = font or pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(label, True, Colors.WHITE.value)
        self.bg_color = color
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
        screen.blit(
            self.text_surface,
            (
                self.rect.centerx - self.text_surface.get_width() // 2,
                self.rect.centery - self.text_surface.get_height() // 2
            )
        )

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)