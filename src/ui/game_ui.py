from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.bar import Bar
from ui.button import Button


def get_bar_positions():
    bar_width = 200
    bar_height = 20
    bar_x = 100
    hunger_bar_y = 20
    boredom_bar_y = hunger_bar_y + bar_height + 30
    return bar_x, bar_width, bar_height, hunger_bar_y, boredom_bar_y


class GameUI:
    """
    Klasa reprezentująca interfejs użytkownika gry, odpowiedzialna za rysowanie elementów interfejsu oraz zarządzanie ich stanem.

    Atrybuty:
        font (Font): Czcionka używana do renderowania tekstu na ekranie.
        hunger_bar (Bar): Pasek reprezentujący poziom głodu.
        boredom_bar (Bar): Pasek reprezentujący poziom znudzenia.
        launch_button (Button): Przycisk uruchamiający tryb zabawy.
        feed_button (Button): Przycisk karmienia zwierzęcia.
        cupcake_button (Button): Przycisk podawania babeczki.
    """
    def __init__(self, font):
        """
            Inicjalizuje interfejs użytkownika gry, tworząc paski stanu oraz przyciski.

            Args:
                font (Font): Czcionka używana do renderowania tekstu na ekranie.
        """
        self.font = font
        self._initialize_bars()
        self._initialize_buttons()

    def _initialize_bars(self):
        bar_x, bar_width, bar_height, hunger_bar_y, boredom_bar_y = get_bar_positions()
        self.hunger_bar = Bar(bar_x, hunger_bar_y, bar_width, bar_height, Colors.BROWN.value, Colors.WHITE.value)
        self.boredom_bar = Bar(bar_x, boredom_bar_y, bar_width, bar_height, Colors.BLUE.value, Colors.WHITE.value)

    def _initialize_buttons(self):
        button_width, button_height = 150, 40
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = SCREEN_HEIGHT - 60
        
        self.launch_button = Button(button_x, button_y, button_width, button_height, 
                                  "Play TIME! :3", font=self.font, 
                                  color=Colors.DARK_VIOLET_BUTTON.value)

        feed_x = button_x - button_width - 20
        self.feed_button = Button(feed_x, button_y, button_width, button_height, 
                                "Feed Me :3", font=self.font, 
                                color=Colors.GREEN.value)

        cupcake_x = button_x + button_width + 20
        self.cupcake_button = Button(cupcake_x, button_y, button_width, button_height,
                               "Cupcake :3", font=self.font, 
                               color=Colors.BLUE.value)

    def draw_status_bars(self, screen):
        """
            Rysuje paski stanu na ekranie, takie jak poziom głodu i znudzenia.

            Args:
                screen (Surface): Powierzchnia ekranu, na której paski mają być narysowane.
        """
        hunger_label = self.font.render("Hunger", True, Colors.TEXT_COLOR.value)
        screen.blit(hunger_label, (self.hunger_bar.x - 90, self.hunger_bar.y + 2))
        self.hunger_bar.draw(screen, rounded=True)

        boredom_label = self.font.render("Boredom", True, Colors.TEXT_COLOR.value)
        screen.blit(boredom_label, (self.boredom_bar.x - 90, self.boredom_bar.y + 2))
        self.boredom_bar.draw(screen, rounded=True)

    def draw_animal_info(self, screen, animal_name, animal_age, position):
        """
            Rysuje informacje o zwierzęciu, takie jak jego imię i wiek.

            Args:
                screen (Surface): Powierzchnia ekranu, na której informacje mają być narysowane.
                animal_name (str): Imię zwierzęcia.
                animal_age (int): Wiek zwierzęcia.
                position (Rect): Pozycja zwierzęcia na ekranie.
        """
        name_label = self.font.render(animal_name, True, Colors.TEXT_COLOR.value)
        asset_x = position.centerx - name_label.get_width() // 2
        asset_y = position.bottom + 50
        screen.blit(name_label, (asset_x, asset_y))

        age_label = self.font.render(f"Age: {animal_age}", True, Colors.TEXT_COLOR.value)
        age_rect = age_label.get_rect(center=(SCREEN_WIDTH // 2, 10))
        screen.blit(age_label, age_rect)

    def draw_timer_and_status(self, screen, game_logic, feed_cooldown):
        """
            Rysuje licznik czasu oraz status trybu gry.

            Args:
                screen (Surface): Powierzchnia ekranu, na której licznik i status mają być narysowane.
                game_logic (GameLogic): Logika gry, zawierająca informacje o trybie gry.
                feed_cooldown (int): Czas pozostały do możliwości karmienia.
        """
        y_offset = 20

        if game_logic.launch_mode:
            seconds_left = max(0, int(game_logic.playtime_remaining / 1000))
            timer_text = f"Time Left: {seconds_left}s"
            y_offset = self._draw_status_text(screen, timer_text, Colors.TEXT_COLOR.value, y_offset)

            status_text = "Playtime mode: ON"
            status_color = Colors.GREEN.value
            y_offset = self._draw_status_text(screen, status_text, status_color, y_offset + 5)

        elif game_logic.in_cooldown:
            cooldown_seconds = max(0, int(game_logic.cooldown_timer / 1000) + 1)
            cooldown_text = f"Cooldown: {cooldown_seconds}s"
            y_offset = self._draw_status_text(screen, cooldown_text, Colors.RED.value, y_offset)

            status_text = "Playtime mode: OFF"
            status_color = Colors.RED.value
            y_offset = self._draw_status_text(screen, status_text, status_color, y_offset + 5)

        else:
            status_text = "Playtime Mode: OFF"
            status_color = Colors.RED.value
            y_offset = self._draw_status_text(screen, status_text, status_color, y_offset)

        if feed_cooldown > 0:
            seconds_left = max(0, int(feed_cooldown / 1000) + 1)
            feed_cooldown_text = f"Feed Cooldown: {seconds_left}s"
            self._draw_status_text(screen, feed_cooldown_text, Colors.RED.value, y_offset + 10)

    def _draw_status_text(self, screen, text, color, y_offset):
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(topright=(SCREEN_WIDTH - 20, y_offset))
        screen.blit(surface, rect)
        return rect.bottom

    def draw_food_info(self, screen, remaining_food):
        """
            Rysuje informacje o pozostałej ilości jedzenia.

            Args:
                screen (Surface): Powierzchnia ekranu, na której informacje mają być narysowane.
                remaining_food (int): Ilość pozostałego jedzenia.
        """
        if remaining_food is not None:
            text = f"Food left: {remaining_food}"
            label_surface = self.font.render(text, True, Colors.TEXT_COLOR.value)
            label_rect = label_surface.get_rect(center=(self.feed_button.rect.centerx, self.feed_button.rect.top-20))
            screen.blit(label_surface, label_rect)

    def update_button_states(self, game_logic, feed_cooldown):
        """
            Aktualizuje stan przycisków na podstawie logiki gry i czasu odnowienia karmienia.

            Args:
                game_logic (GameLogic): Logika gry, zawierająca informacje o trybie gry.
                feed_cooldown (int): Czas pozostały do możliwości karmienia.
        """
        if not game_logic.in_cooldown and not game_logic.launch_mode:
            self.launch_button.set_enabled(True)
        else:
            self.launch_button.set_enabled(False)

        if feed_cooldown > 0 or game_logic.launch_mode:
            self.feed_button.set_enabled(False)
        else:
            self.feed_button.set_enabled(True)

        if game_logic.launch_mode:
            self.cupcake_button.set_enabled(False)
        else:
            self.cupcake_button.set_enabled(True)