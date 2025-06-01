import pygame
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene

class GameScene(BaseScene):
    def __init__(self, animal):
        self.font = pygame.font.SysFont(None, 72)
        self.text = self.font.render("Game Started!", True, Colors.WHITE.value)
        self.animal = animal

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def draw(self, screen):
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.text, (SCREEN_WIDTH // 2 - self.text.get_width() // 2, SCREEN_HEIGHT // 2 - self.text.get_height() - 50))