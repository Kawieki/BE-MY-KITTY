import pygame
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.button import Button
from managers.font_manager import FontManager
from managers.save_manager import SaveManager

class SaveMenuScene(BaseScene):
    """
    Scena menu zapisu gry, umożliwiająca użytkownikowi zapisanie aktualnego stanu gry lub powrót do rozgrywki.

    Atrybuty:
        game_scene (GameScene): Obiekt sceny gry, której stan ma zostać zapisany.
        save_manager (SaveManager): Menedżer odpowiedzialny za zapisywanie stanu gry.
        buttons (list[Button]): Lista przycisków dostępnych w menu zapisu.
    """
    def __init__(self, game_scene):
        """
            Inicjalizuje scenę menu zapisu gry, ustawiając przyciski oraz odniesienie do sceny gry.

            Args:
                game_scene (GameScene): Obiekt sceny gry, której stan ma zostać zapisany.
        """
        self.game_scene = game_scene
        self.save_manager = SaveManager()
        button_width, button_height = 200, 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.buttons = [
            Button(button_x, SCREEN_HEIGHT // 2 - 50, button_width, button_height,
                  "Save Game", font=FontManager.get_font("Boldins"),
                  color=Colors.BUTTON_PINK.value),
            Button(button_x, SCREEN_HEIGHT // 2 + 50, button_width, button_height,
                  "Back to Game", font=FontManager.get_font("Boldins"),
                  color=Colors.BUTTON_PINK.value)
        ]

    def handle_events(self, events):
        """
            Obsługuje zdarzenia użytkownika, takie jak kliknięcia myszą oraz naciśnięcia klawiszy.

            Args:
                events (list[Event]): Lista zdarzeń do obsłużenia.

            Returns:
                Scene: Nowa scena, jeśli użytkownik wybrał opcję z menu zapisu, w przeciwnym razie `None`.
         """

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.label == "Save Game":
                            self._save_current_game()
                        elif button.label == "Back to Game":
                            return self.game_scene
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.game_scene

    def _save_current_game(self):
        success = self.save_manager.save_game(
            self.game_scene.animal,
            self.game_scene.food_manager,
            self.game_scene.game_logic
        )
        if success:
            self.show_success = True

    def draw(self, screen):
        """
            Rysuje scenę menu zapisu gry, w tym półprzezroczyste tło, tytuł oraz przyciski.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
        """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.DARK_GRAY.value)
        screen.blit(overlay, (0, 0))

        title_font = FontManager.get_font("Boldins")
        title = title_font.render("SAVE GAME", True, Colors.WHITE.value)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

        if hasattr(self, 'show_success') and self.show_success:
            success_text = title_font.render("Game Saved Successfully!", True, Colors.GREEN.value)
            success_rect = success_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            screen.blit(success_text, success_rect) 