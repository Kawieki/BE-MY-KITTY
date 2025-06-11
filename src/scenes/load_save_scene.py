import pygame
from entities.animal import Animal
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.button import Button
from managers.font_manager import FontManager
from managers.save_manager import SaveManager
from scenes.game_scene import GameScene
from utils.animated_asset import AnimatedAsset
from utils.asset import Asset

class LoadSaveScene(BaseScene):
    """
    Scena ładowania zapisanej gry, umożliwiająca użytkownikowi wybór zapisu do wczytania.

    Atrybuty:
        font (Font): Czcionka używana do wyświetlania tekstu.
        save_manager (SaveManager): Menedżer zapisów gry.
        save_files (list[str]): Lista nazw plików zapisów gry.
        buttons (list[Button]): Lista przycisków odpowiadających zapisom gry.
        back_button (Button): Przycisk powrotu do menu głównego.
    """
    def __init__(self):
        """
            Inicjalizuje scenę ładowania zapisów gry, tworząc przyciski dla dostępnych zapisów oraz przycisk powrotu.
        """
        self.font = FontManager.get_font("Boldins")
        self.save_manager = SaveManager()
        self.save_files = self.save_manager.get_recent_saves()
        self.buttons = []
        button_width = 400
        button_height = 60
        spacing = 20
        start_y = SCREEN_HEIGHT // 2 - (len(self.save_files) * (button_height + spacing)) // 2
        
        for i, save_file in enumerate(self.save_files):
            y = start_y + i * (button_height + spacing)
            self.buttons.append(Button(
                SCREEN_WIDTH // 2 - button_width // 2,
                y,
                button_width,
                button_height,
                save_file,
                font=self.font,
                color=Colors.BUTTON_PINK.value
            ))

        self.back_button = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT - 100,
            200,
            50,
            "Back",
            font=self.font,
            color=Colors.BUTTON_PINK.value
        )

    def handle_events(self, events):
        """
            Obsługuje zdarzenia użytkownika, takie jak kliknięcia myszą.

            Args:
                events (list[Event]): Lista zdarzeń do obsłużenia.

            Returns:
                Scene: Nowa scena, jeśli użytkownik wybrał zapis lub kliknął przycisk powrotu, w przeciwnym razie `None`.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.back_button.is_clicked(mouse_pos):
                    from scenes.menu_scene import MenuScene
                    return MenuScene()

                for save_file in self.save_files:
                    button = next(btn for btn in self.buttons if btn.label == save_file)
                    if button.is_clicked(mouse_pos):
                        save_data = self.save_manager.load_game(save_file)
                        if save_data:
                            return create_game_state(save_data)
        return None

    def draw(self, screen):
        """
            Rysuje scenę ładowania zapisów gry, w tym tło, tytuł oraz przyciski.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
            """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(Colors.BLACK.value)
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        title = self.font.render("Load Save", True, Colors.WHITE.value)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for button in self.buttons:
            button.draw(screen)
        self.back_button.draw(screen)

def create_game_state(save_data):
    """
        Tworzy stan gry na podstawie danych zapisanych w pliku.

        Args:
            save_data (dict): Dane zapisane w pliku.

        Returns:
            GameScene: Scena gry z odtworzonym stanem.
    """
    static_asset = Asset(
        save_data.get("static_asset_path"),
        save_data.get("static_asset_size"),
        save_data.get("static_asset_position"),
        label=save_data.get("label")
    )

    animated_asset = AnimatedAsset(
        folder=save_data.get("animated_asset_path"),
        size=save_data.get("animated_asset_size"),
        pos=save_data.get("animated_asset_position")
    )

    animal = Animal(
        static_asset=static_asset,
        name=save_data.get("name"),
        age=save_data.get("age"),
        animated_asset=animated_asset
    )

    food_quantity = save_data.get("quantity")
    playtime = save_data.get("playtime")
    game_scene = GameScene(animal, food_quantity, playtime)
    game_scene.food_manager.food_quantity = food_quantity
    game_scene.food_manager.remaining_food = save_data.get("remaining")
    game_scene.game_logic.animal.hunger_level = save_data.get("hunger_level")
    game_scene.game_logic.animal.boredom_level = save_data.get("boredom_level")
    game_scene.game_logic.playtime_remaining = save_data.get("playtime_remaining")
    game_scene.game_logic.in_cooldown = bool(save_data.get("in_cooldown"))
    game_scene.game_logic.cooldown_timer = save_data.get("cooldown_timer")
    return game_scene
