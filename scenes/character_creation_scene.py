import pygame

from scenes.character_settings_scene import CharacterSettingsScene
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.button import Button
from utils.Asset import Asset

class CharacterCreationScene(BaseScene):
    def __init__(self):
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font.render("Choose Character", True, Colors.WHITE.value)
        self.buttons = [
            Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100, 250, 50, "Back To Menu")
        ]

        self.character_assets = []
        asset_data = [
            ("assets/characters/hello_kitty.png", "Hello Kitty"),
            ("assets/characters/kuromi.png", "Kuromi"),
            ("assets/characters/melody.png", "Melody"),
            ("assets/characters/cinnamoroll.png", "Cinnamoroll"),
        ]

        asset_width, asset_height = 125, 125
        spacing = (SCREEN_WIDTH - len(asset_data) * asset_width) // (len(asset_data) + 1)

        for i, (path, label) in enumerate(asset_data):
            x_position = spacing + i * (asset_width + spacing)
            y_position = SCREEN_HEIGHT // 2 - 150
            self.character_assets.append(
                Asset(path, (asset_width, asset_height), (x_position, y_position), label=label))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for asset in self.character_assets:
                    if asset.image.get_rect(topleft=asset.position).collidepoint(mouse_pos):
                        return CharacterSettingsScene(asset)
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.label == "Back To Menu":
                            from scenes.menu_scene import MenuScene
                            return MenuScene()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 50))

        for asset in self.character_assets:
            asset.draw(screen)

        for button in self.buttons:
            button.draw(screen)