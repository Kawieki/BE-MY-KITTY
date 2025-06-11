import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, Colors, FALL_SPEED, SPEED_TIMER, SPEED_INTERVAL, SPEED_INCREMENT
from utils.functional_asset import FunctionalAsset
from random import randint
from settings import CHARACTER_SPEED, CUPCAKE_SPAWN_DELAY

class CupcakeMode:
    """
    Tryb Cupcake - minigra w grze, w której gracz zbiera spadające babeczki.

    Atrybuty:
        cupcakes (list): Lista obiektów babeczek obecnych na ekranie.
        collected_cupcakes (int): Liczba zebranych babeczek.
        missed_cupcakes (int): Liczba babeczek, które zostały pominięte.
        highest_score (int): Najwyższy wynik osiągnięty przez gracza.
        spawn_timer (float): Licznik czasu do wygenerowania nowej babeczki.
        spawn_delay (float): Opóźnienie między generowaniem kolejnych babeczek.
        character_speed (float): Prędkość poruszania się postaci gracza.
        is_active (bool): Flaga wskazująca, czy tryb Cupcake jest aktywny.
        game_over (bool): Flaga wskazująca, czy gra w trybie Cupcake została zakończona.
        fall_speed (float): Prędkość spadania babeczek.
        speed_timer (float): Licznik czasu do zwiększenia prędkości spadania babeczek.
        speed_interval (float): Interwał czasu między kolejnymi zwiększeniami prędkości spadania.
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
           Włącza lub wyłącza tryb Cupcake.

           Parametry:
               character_position (Rect, opcjonalny): Pozycja postaci gracza. Jeśli tryb zostanie wyłączony,
               postać zostanie ustawiona na środku ekranu.

           Zwraca:
               bool: True, jeśli tryb Cupcake został włączony, False, jeśli został wyłączony.
           """
        ...
        self.is_active = not self.is_active
        self.game_over = False
        if not self.is_active:
            self.reset()
            if character_position:
                character_position.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        return self.is_active

    def update(self, dt, character_position, character_rect):
        """
           Aktualizuje logikę trybu Cupcake, w tym pozycję postaci, generowanie babeczek
           oraz sprawdzanie kolizji.

           Parametry:
               dt (float): Delta czasu od ostatniej aktualizacji.
               character_position (Vector2): Pozycja postaci gracza.
               character_rect (Rect): Prostokąt określający rozmiar i pozycję postaci gracza.
           """
        if not self.is_active or self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            character_position.y -= self.character_speed * dt
        if keys[pygame.K_s]:
            character_position.y += self.character_speed * dt
        if keys[pygame.K_a]:
            character_position.x -= self.character_speed * dt
        if keys[pygame.K_d]:
            character_position.x += self.character_speed * dt

        character_position.x = max(0, min(character_position.x, SCREEN_WIDTH - character_rect.width))
        character_position.y = max(0, min(character_position.y, SCREEN_HEIGHT - character_rect.height))

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self._spawn_cupcake()
            self.spawn_timer = 0

        self.speed_timer += dt
        if self.speed_timer >= self.speed_interval:
            self.fall_speed += self.speed_increment
            self.speed_timer = 0

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
            Generuje nową babeczkę na ekranie w losowej pozycji.
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
            Rysuje babeczki, licznik punktów oraz komunikat o zakończeniu gry na ekranie.

            Parametry:
                screen (Surface): Powierzchnia ekranu, na której elementy mają być narysowane.
                font (Font): Czcionka używana do rysowania tekstu.
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
            Resetuje stan trybu Cupcake
        """
        self.cupcakes.clear()
        self.collected_cupcakes = 0
        self.missed_cupcakes = 0
        self.spawn_timer = 0
        self.fall_speed = 200
        self.speed_timer = 0
        self.is_active = False
        self.game_over = False