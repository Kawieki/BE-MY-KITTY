import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, Colors, FALL_SPEED, SPEED_TIMER, SPEED_INTERVAL, SPEED_INCREMENT
from utils.functional_asset import FunctionalAsset
from random import randint
from settings import CHARACTER_SPEED, CUPCAKE_SPAWN_DELAY

class CupcakeMode:
    """
        Tryb gry "Cupcake Mode", w którym gracz zbiera spadające babeczki.

        Atrybuty:
            cupcakes (list): Lista obiektów babeczek obecnych na ekranie.
            collected_cupcakes (int): Liczba zebranych babeczek.
            missed_cupcakes (int): Liczba pominiętych babeczek.
            highest_score (int): Najwyższy wynik osiągnięty przez gracza.
            spawn_timer (float): Timer kontrolujący czas między pojawieniem się kolejnych babeczek.
            spawn_delay (float): Opóźnienie między pojawieniem się kolejnych babeczek.
            character_speed (float): Prędkość poruszania się postaci gracza.
            is_active (bool): Flaga wskazująca, czy tryb gry jest aktywny.
            game_over (bool): Flaga wskazująca, czy gra się zakończyła.
            fall_speed (float): Prędkość spadania babeczek.
            speed_timer (float): Timer kontrolujący wzrost prędkości spadania babeczek.
            speed_interval (float): Interwał czasu między wzrostami prędkości spadania babeczek.
            speed_increment (float): Wartość, o którą zwiększa się prędkość spadania babeczek.
    """
    def __init__(self):
        self.cupcakes = []
        self.collected_cupcakes = 0
        self.missed_cupcakes = 0
        self.highest_score = 0
        self.spawn_timer = 0
        self.spawn_delay = CUPCAKE_SPAWN_DELAY
        self.character_speed = CHARACTER_SPEED
        self.is_active = False
        self.game_over = False
        self.fall_speed = FALL_SPEED
        self.speed_timer = SPEED_TIMER
        self.speed_interval = SPEED_INTERVAL
        self.speed_increment = SPEED_INCREMENT

    def toggle(self, character_position=None):
        """
            Włącza lub wyłącza tryb gry. Resetuje stan gry, jeśli tryb jest wyłączany.

            Args:
                character_position (Rect, optional): Pozycja postaci gracza. Domyślnie `None`.

            Returns:
                bool: Zwraca `True`, jeśli tryb gry został włączony, w przeciwnym razie `False`.
        """
        self.is_active = not self.is_active
        self.game_over = False
        if not self.is_active:
            self.reset()
            if character_position:
                character_position.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        return self.is_active

    def update(self, dt, character_position, character_rect):
        """
            Aktualizuje stan gry, w tym pozycję postaci, babeczki i logikę kolizji.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
                character_position (Rect): Pozycja postaci gracza.
                character_rect (Rect): Prostokąt określający rozmiar i pozycję postaci gracza.
        """
        if not self.is_active or self.game_over:
            return

        # Logika poruszania się postaci
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            character_position.y -= self.character_speed * dt
        if keys[pygame.K_s]:
            character_position.y += self.character_speed * dt
        if keys[pygame.K_a]:
            character_position.x -= self.character_speed * dt
        if keys[pygame.K_d]:
            character_position.x += self.character_speed * dt

        # Ograniczenie ruchu postaci do granic ekranu
        character_position.x = max(0, min(character_position.x, SCREEN_WIDTH - character_rect.width))
        character_position.y = max(0, min(character_position.y, SCREEN_HEIGHT - character_rect.height))

        # Logika pojawiania się babeczek
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self._spawn_cupcake()
            self.spawn_timer = 0

        # Logika zwiększania prędkości spadania babeczek
        self.speed_timer += dt
        if self.speed_timer >= self.speed_interval:
            self.fall_speed += self.speed_increment
            self.speed_timer = 0

        # Aktualizacja pozycji babeczek i logika kolizji
        for cupcake in self.cupcakes[:]:
            cupcake.rect.y += self.fall_speed * (dt / 1000)

            if cupcake.rect.colliderect(character_rect):
                self.cupcakes.remove(cupcake)
                self.collected_cupcakes += 1
                if self.collected_cupcakes > self.highest_score:
                    self.highest_score = self.collected_cupcakes
            elif cupcake.rect.top > SCREEN_HEIGHT:
                self.cupcakes.remove(cupcake)
                self.missed_cupcakes += 1
                if self.missed_cupcakes >= 5:
                    self.game_over = True

    def _spawn_cupcake(self):
        """
            Tworzy nową babeczkę i dodaje ją do listy babeczek.
        """
        margin = 50
        width = 60
        height = int(width * (466 / 348))
        x = randint(margin, SCREEN_WIDTH - margin - width)
        y = -height
        cupcake = FunctionalAsset("assets/cupcake.png", (width, height), (x, y))
        self.cupcakes.append(cupcake)

    def draw(self, screen, font):
        """
            Rysuje babeczki oraz informacje o stanie gry na ekranie.

            Args:
                screen (Surface): Powierzchnia Pygame, na której elementy mają być narysowane.
                font (Font): Czcionka używana do wyświetlania tekstu.
        """
        if not self.is_active:
            return

        for cupcake in self.cupcakes:
            cupcake.draw(screen)

        counter_text = f"Cupcakes: {self.collected_cupcakes} | Missed: {self.missed_cupcakes} | High Score: {self.highest_score}"
        counter_surface = font.render(counter_text, True, Colors.DARK_VIOLET_BUTTON.value)
        screen.blit(counter_surface, (SCREEN_WIDTH - counter_surface.get_width() - 20, 20))

        if self.game_over:
            game_over_text = font.render("GAME OVER - YOU'VE LOST 5 CUPCAKES!", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def reset(self):
        """
           Resetuje stan gry do wartości początkowych.
        """
        self.cupcakes.clear()
        self.collected_cupcakes = 0
        self.missed_cupcakes = 0
        self.spawn_timer = 0
        self.fall_speed = 200
        self.speed_timer = 0
        self.is_active = False
        self.game_over = False