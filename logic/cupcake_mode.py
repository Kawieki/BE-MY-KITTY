import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, Colors, FALL_SPEED, SPEED_TIMER, SPEED_INTERVAL, SPEED_INCREMENT
from utils.functional_asset import FunctionalAsset
from random import randint
from settings import CHARACTER_SPEED, CUPCAKE_SPAWN_DELAY

class CupcakeMode:
    def __init__(self):
        self.cupcakes = []
        self.collected_cupcakes = 0
        self.missed_cupcakes = 0
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
        self.is_active = not self.is_active
        self.game_over = False
        if not self.is_active:
            self.reset()
            if character_position:
                character_position.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        return self.is_active

    def update(self, dt, character_position, character_rect):
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
            elif cupcake.rect.top > SCREEN_HEIGHT:
                self.cupcakes.remove(cupcake)
                self.missed_cupcakes += 1
                if self.missed_cupcakes >= 5:
                    self.game_over = True

    def _spawn_cupcake(self):
        margin = 50
        width = 60
        height = int(width * (466 / 348))
        x = randint(margin, SCREEN_WIDTH - margin - width)
        y = -height
        cupcake = FunctionalAsset("assets/cupcake.png", (width, height), (x, y))
        self.cupcakes.append(cupcake)

    def draw(self, screen, font):
        if not self.is_active:
            return

        for cupcake in self.cupcakes:
            cupcake.draw(screen)

        counter_text = f"Cupcakes: {self.collected_cupcakes} | Missed: {self.missed_cupcakes}"
        counter_surface = font.render(counter_text, True, Colors.DARK_VIOLET_BUTTON.value)
        screen.blit(counter_surface, (SCREEN_WIDTH - counter_surface.get_width() - 20, 20))

        if self.game_over:
            game_over_text = font.render("KONIEC GRY - Zgubiłeś 5 babeczek!", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def reset(self):
        self.cupcakes.clear()
        self.collected_cupcakes = 0
        self.missed_cupcakes = 0
        self.spawn_timer = 0
        self.fall_speed = 200
        self.speed_timer = 0
        self.is_active = False
        self.game_over = False