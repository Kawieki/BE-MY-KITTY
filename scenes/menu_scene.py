import pygame

from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.button import Button
from scenes.character_creation_scene import CharacterCreationScene

class MenuScene(BaseScene):
    def __init__(self):
        self.font = pygame.font.SysFont(None, 72)
        self.title = self.font.render("Main Menu", True, Colors.WHITE.value)

        self.buttons = [
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Start Game"),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Exit")
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.text == "Start Game":
                            return CharacterCreationScene()
                        elif button.text == "Exit":
                            pygame.quit()
                            exit()

    def draw(self, screen):
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 50))

        for button in self.buttons:
            button.draw(screen)