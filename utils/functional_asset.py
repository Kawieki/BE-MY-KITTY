import pygame
from utils.asset import Asset

class FunctionalAsset(Asset):
    def __init__(self, path, size, position, label=None, font_size=24, font_color=(255, 255, 255)):
        super().__init__(path, size, position, label, font_size, font_color)
        self.rect = pygame.Rect(position, size)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
                self.position = (self.rect.x, self.rect.y)
                return True

        return False

    def draw(self, screen):
        self.position = (self.rect.x, self.rect.y)
        super().draw(screen)
