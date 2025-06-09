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
        self.enabled = True

    def set_enabled(self, enabled):
        self.enabled = enabled

    def draw(self, screen):
        bg_color = self.bg_color if self.enabled else (100, 100, 100)
        text_color = Colors.WHITE.value if self.enabled else (180, 180, 180)

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.label, True, text_color)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, mouse_pos):
        return self.enabled and self.rect.collidepoint(mouse_pos)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)