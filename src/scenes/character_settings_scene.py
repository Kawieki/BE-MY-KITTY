import pygame
from src.entities.animal import Animal
from src.scenes.base_scene import BaseScene
from src.scenes.game_scene import GameScene
from src.settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.button import Button
from src.utils.animated_asset import AnimatedAsset


def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s"


def _adjustment_keys():
    return [
        "age_up", "age_down",
        "food_up", "food_down",
        "playtime_up", "playtime_down"
    ]


class CharacterSettingsScene(BaseScene):
    """
    Scena ustawień postaci, umożliwiająca konfigurację wybranej postaci przed rozpoczęciem gry.

    Atrybuty:
        selected_character (Asset): Wybrana postać, której ustawienia są konfigurowane.
        font (Font): Czcionka używana do wyświetlania tekstu.
        title (Surface): Powierzchnia tekstu tytułu sceny.
        character_data (dict): Dane postaci, takie jak imię, wiek, ilość jedzenia i czas zabawy.
        input_boxes (dict): Słownik zawierający prostokąty pól wejściowych dla danych postaci.
        active_box (str): Klucz aktywnego pola wejściowego (jeśli istnieje).
        user_inputs (dict): Dane wprowadzone przez użytkownika.
        adjustment_buttons (dict): Słownik przycisków do zmiany wartości danych postaci.
        play_button (Button): Przycisk rozpoczynający grę.
        holding_flags (dict): Flagi określające, które przyciski są aktualnie wciśnięte.
        hold_timer (dict): Słownik przechowujący czas ostatniego wciśnięcia przycisków.
        hold_delay (int): Opóźnienie między kolejnymi zmianami wartości przytrzymanych przycisków.
    """
    def __init__(self, selected_character):
        """
            Inicjalizuje scenę ustawień postaci, ustawiając wybraną postać, dane postaci, pola wejściowe, przyciski oraz inne elementy interfejsu.

            Args:
                selected_character (Asset): Wybrana postać, której ustawienia są konfigurowane.
            """
        self.selected_character = selected_character
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font.render(self.selected_character.label, True, Colors.WHITE.value)
        self.character_data = {
            "Name": "",
            "Age": 0,
            "Food": 1,
            "Playtime": 5,
        }

        self.input_boxes = {
            key: pygame.Rect(SCREEN_WIDTH // 2 - 100, 200 + i * 60, 200, 40)
            for i, key in enumerate(self.character_data)
        }

        self.active_box = None
        self.user_inputs = {k: v for k, v in self.character_data.items()}
        self._create_adjustment_buttons()
        self.play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Play")
        self.holding_flags = {key: False for key in _adjustment_keys()}
        self.hold_timer = {key: 0 for key in self.holding_flags}
        self.hold_delay = 100

    def _create_adjustment_buttons(self):
        button_specs = [
            ("Age", 260),
            ("Food", 320),
            ("Playtime", 380),
        ]

        self.adjustment_buttons = {}

        for label, y in button_specs:
            up_key = f"{label.lower()}_up"
            down_key = f"{label.lower()}_down"
            up_btn = Button(SCREEN_WIDTH // 2 + 110, y, 40, 40, "+", font_size=32, color=Colors.GREEN.value)
            down_btn = Button(up_btn.rect.x + up_btn.rect.width + 10, y, 40, 40, "-", font_size=32, color=Colors.RED.value)
            self.adjustment_buttons[up_key] = up_btn
            self.adjustment_buttons[down_key] = down_btn

    def handle_events(self, events):
        """
            Obsługuje zdarzenia użytkownika, takie jak kliknięcia myszą, wprowadzanie tekstu i przytrzymywanie przycisków.

            Args:
                events (list[Event]): Lista zdarzeń do obsłużenia.

            Returns:
                Scene: Nowa scena, jeśli użytkownik kliknął przycisk "Play", w przeciwnym razie `None`.
             """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = self._handle_mouse_down(event.pos)
                if result:
                    return result

            elif event.type == pygame.MOUSEBUTTONUP:
                self._reset_holding_flags()

            elif event.type == pygame.KEYDOWN and self.active_box == "Name":
                self._handle_text_input(event)

    def _handle_mouse_down(self, mouse_pos):
        if self.input_boxes["Name"].collidepoint(mouse_pos):
            self.active_box = "Name"
        else:
            self.active_box = None

        if self.play_button.is_clicked(mouse_pos):
            return self._start_game()

        for key, button in self.adjustment_buttons.items():
            if button.is_clicked(mouse_pos):
                self.holding_flags[key] = True
        return None

    def _reset_holding_flags(self):
        for key in self.holding_flags:
            self.holding_flags[key] = False

    def _handle_text_input(self, event):
        name = self.user_inputs["Name"]
        if event.key == pygame.K_RETURN:
            self.active_box = None
        elif event.key == pygame.K_BACKSPACE:
            self.user_inputs["Name"] = name[:-1]
        elif len(name) < 10:
            self.user_inputs["Name"] += event.unicode

    def _start_game(self):
        animated_asset = AnimatedAsset(
            folder=f"assets/characters/{self.selected_character.name}_frames",
            size=self.selected_character.image.get_size(),
            pos=(SCREEN_WIDTH // 2 - self.selected_character.image.get_width() // 2,
                 SCREEN_HEIGHT // 2 - self.selected_character.image.get_height() // 2)
        )
        animal = Animal(
            name=self.user_inputs["Name"],
            age=self.character_data["Age"],
            static_asset=self.selected_character,
            animated_asset=animated_asset
        )
        return GameScene(animal, self.character_data["Food"], self.character_data["Playtime"])

    def update(self, dt):
        """
            Aktualizuje logikę sceny, w tym obsługę przytrzymanych przycisków.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        current_time = pygame.time.get_ticks()
        for key, flag in self.holding_flags.items():
            if flag and current_time - self.hold_timer[key] >= self.hold_delay:
                self._adjust_value(key)
                self.hold_timer[key] = current_time

    def _adjust_value(self, key):
        if key == "age_up":
            self.character_data["Age"] += 1
        elif key == "age_down":
            self.character_data["Age"] = max(0, self.character_data["Age"] - 1)
        elif key == "food_up":
            self.character_data["Food"] = min(100, self.character_data["Food"] + 1)
        elif key == "food_down":
            self.character_data["Food"] = max(1, self.character_data["Food"] - 1)
        elif key == "playtime_up":
            self.character_data["Playtime"] = min(180, self.character_data["Playtime"] + 1)
        elif key == "playtime_down":
            self.character_data["Playtime"] = max(5, self.character_data["Playtime"] - 1)

    def draw(self, screen):
        """
            Rysuje scenę na ekranie, w tym wybraną postać, pola wejściowe, przyciski i inne elementy interfejsu.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
        """
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 10))

        self._draw_character(screen)
        self._draw_input_fields(screen)
        self._draw_buttons(screen)

    def _draw_character(self, screen):
        name_box = self.input_boxes["Name"]
        x = SCREEN_WIDTH // 2 - self.selected_character.image.get_width() // 2
        y = name_box.y - self.selected_character.image.get_height() - 10
        screen.blit(self.selected_character.image, (x, y))

    def _draw_input_fields(self, screen):
        for key, box in self.input_boxes.items():
            label = self.font.render(f"{key}:", True, Colors.WHITE.value)
            screen.blit(label, (box.x - label.get_width() - 10, box.y + 5))
            pygame.draw.rect(screen, Colors.BLUE.value if key == self.active_box else Colors.WHITE.value, box, 2)
            text = self._get_display_text(key)
            text_surf = self.font.render(text, True, Colors.WHITE.value)
            screen.blit(text_surf, (box.x + 5, box.y + 5))

    def _get_display_text(self, key):
        if key == "Name":
            return self.user_inputs[key]
        if key == "Food":
            return f"{self.character_data[key]}"
        if key == "Playtime":
            return format_time(self.character_data[key])
        return str(self.character_data[key])

    def _draw_buttons(self, screen):
        for button in self.adjustment_buttons.values():
            button.draw(screen)
        self.play_button.draw(screen)
