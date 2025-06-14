import pygame
from src.settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.managers.font_manager import FontManager
from src.scenes.save_menu_scene import SaveMenuScene

class PauseMenuScene(BaseScene):
    """
    Scena menu pauzy, umożliwiająca użytkownikowi wstrzymanie gry, zapisanie stanu gry lub zakończenie rozgrywki.

    Atrybuty:
        game_scene (GameScene): Obiekt sceny gry, który został wstrzymany.
        buttons (list[Button]): Lista przycisków dostępnych w menu pauzy.
    """
    def __init__(self, game_scene):
        """
            Inicjalizuje scenę menu pauzy, ustawiając przyciski oraz odniesienie do wstrzymanej sceny gry.

            Args:
                game_scene (GameScene): Obiekt sceny gry, który został wstrzymany.
        """
        self.game_scene = game_scene
        self.buttons = [
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, 
                  "Resume Game", font=FontManager.get_font("Boldins"), 
                  color=Colors.BUTTON_PINK.value),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, 
                  "Save Game", font=FontManager.get_font("Boldins"), 
                  color=Colors.BUTTON_PINK.value),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, 
                  "Quit Game", font=FontManager.get_font("Boldins"), 
                  color=Colors.BUTTON_PINK.value)
        ]

    def handle_events(self, events):
        """
            Obsługuje zdarzenia użytkownika, takie jak kliknięcia myszą oraz naciśnięcia klawiszy.

            Args:
                events (list[Event]): Lista zdarzeń do obsłużenia.

            Returns:
                Scene: Nowa scena, jeśli użytkownik wybrał opcję z menu pauzy, w przeciwnym razie `None`.
            """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button in self.buttons:
                    if button.is_clicked(mouse_pos):
                        if button.label == "Resume Game":
                            return self.game_scene
                        elif button.label == "Save Game":
                            return SaveMenuScene(self.game_scene)
                        elif button.label == "Quit Game":
                            from src.scenes.menu_scene import MenuScene
                            return MenuScene()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.game_scene

    def draw(self, screen):
        """
            Rysuje scenę menu pauzy, w tym półprzezroczyste tło, tytuł oraz przyciski.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
         """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(Colors.DARK_GRAY.value)
        screen.blit(overlay, (0, 0))

        title_font = FontManager.get_font("Boldins")
        title = title_font.render("PAUSED", True, Colors.WHITE.value)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen) 