import pygame

from scenes.character_settings_scene import CharacterSettingsScene
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.button import Button
from scenes.game_scene import GameScene
from utils.AnimatedAsset import AnimatedAsset
from utils.Asset import Asset


class CharacterCreationScene(BaseScene):
    def __init__(self):
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font.render("Choose Character", True, Colors.WHITE.value)

        self.buttons = [
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Start Game")
        ]

        self.character_assets = [
            Asset("assets/hello_kitty.png", (125, 125), (SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT // 2 - 150), label="Hello Kitty"),
            Asset("assets/kuromi.png", (125, 125), (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 150), label="Kuromi"),
        ]

        self.animated_asset = AnimatedAsset(
            "assets/test_frames", (125, 125), (3 * SCREEN_WIDTH // 4 - 50, SCREEN_HEIGHT // 2 - 150)
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for asset in self.character_assets:
                    if asset.image.get_rect(topleft=asset.position).collidepoint(mouse_pos):
                        return CharacterSettingsScene(asset)
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.text == "Start Game":
                            return GameScene()
    def update(self, dt):
        self.animated_asset.update(dt)

    def draw(self, screen):
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 50))

        for asset in self.character_assets:
            asset.draw(screen)

        self.animated_asset.draw(screen)

        for button in self.buttons:
            button.draw(screen)