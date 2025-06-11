import pygame

from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.button import Button
from scenes.character_creation_scene import CharacterCreationScene
from managers.font_manager import FontManager
from scenes.load_save_scene import LoadSaveScene


class MenuScene(BaseScene):
    def __init__(self):
        self.logo = pygame.image.load("assets/logo.png")
        scale_factor = min(SCREEN_WIDTH / 831, SCREEN_HEIGHT / 157) * 0.9
        new_width = int(831 * scale_factor)
        new_height = int(157 * scale_factor)
        self.logo = pygame.transform.scale(self.logo, (new_width, new_height))
        self.buttons = [
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Start Game", font=FontManager.get_font("Boldins"), color=Colors.BUTTON_PINK.value),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Load Save", font=FontManager.get_font("Boldins"), color=Colors.BUTTON_PINK.value),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Exit", font=FontManager.get_font("Boldins"), color=Colors.BUTTON_PINK.value)
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.label == "Start Game":
                            return CharacterCreationScene()
                        elif button.label == "Load Save":
                            return LoadSaveScene()
                        elif button.label == "Exit":
                            pygame.quit()
                            exit()

    def draw(self, screen):
        screen.fill(Colors.PINK_MENU.value)
        screen.blit(self.logo, (SCREEN_WIDTH // 2 - self.logo.get_width() // 2, 50))

        for button in self.buttons:
            button.draw(screen)