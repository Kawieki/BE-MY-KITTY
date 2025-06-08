import pygame

class Asset:
    def __init__(self, path, size, position, label=None, font_size=24, font_color=(255, 255, 255)):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size)
        self.position = position
        self.label = label
        self.name = label.lower().replace(" ", "") if label else None
        self.font_size = font_size
        self.font_color = font_color
        self.label_surface = None
        self.label_position = None

    def initialize_label(self):
        if self.label and not self.label_surface:
            font = pygame.font.SysFont(None, self.font_size)
            self.label_surface = font.render(self.label, True, self.font_color)
            self.label_position = (
                self.position[0] + self.image.get_width() // 2 - self.label_surface.get_width() // 2,
                self.position[1] + self.image.get_height() + 5
            )

    def draw(self, screen):
        screen.blit(self.image, self.position)
        if self.label:
            self.initialize_label()
            screen.blit(self.label_surface, self.label_position)