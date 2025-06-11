import pygame
from src.scenes.character_settings_scene import CharacterSettingsScene
from src.settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.asset import Asset

class CharacterCreationScene(BaseScene):
    """
    Scena tworzenia postaci, umożliwiająca wybór postaci przez użytkownika.

    Atrybuty:
        font (Font): Czcionka używana do wyświetlania tekstu.
        title (Surface): Powierzchnia tekstu tytułu sceny.
        buttons (list[Button]): Lista przycisków dostępnych na scenie.
        character_assets (list[Asset]): Lista zasobów postaci dostępnych do wyboru.
    """
    def __init__(self):
        """
            Inicjalizuje scenę tworzenia postaci, ustawiając czcionkę, tytuł, przyciski oraz zasoby postaci.
        """
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font.render("Choose Character", True, Colors.WHITE.value)

        self.buttons = [
            Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100, 250, 50, "Back To Menu", color=Colors.BUTTON_PINK.value)
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
        """
            Obsługuje zdarzenia użytkownika, takie jak kliknięcia myszą.

            Args:
                events (list[Event]): Lista zdarzeń do obsłużenia.

            Returns:
                   Scene: Nowa scena, jeśli użytkownik wybrał postać lub kliknął przycisk, w przeciwnym razie `None`.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for asset in self.character_assets:
                    if asset.image.get_rect(topleft=asset.position).collidepoint(mouse_pos):
                        return CharacterSettingsScene(asset)
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.label == "Back To Menu":
                            from src.scenes.menu_scene import MenuScene
                            return MenuScene()

    def update(self, dt):
        """
            Aktualizuje logikę sceny.
            Args:
                 dt (float): Czas, który upłynął od ostatniej aktualizacji.
            """
        pass

    def draw(self, screen):
        """
            Rysuje scenę na ekranie.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
        """
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 50))

        for asset in self.character_assets:
            asset.draw(screen)

        for button in self.buttons:
            button.draw(screen)
