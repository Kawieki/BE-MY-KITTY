import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from utils.functional_asset import FunctionalAsset
from random import randint, uniform
from settings import CHARACTER_SPEED, CUPCAKE_SPAWN_DELAY

class CupcakeMode:
    def __init__(self):
        self.cupcakes = []
        self.collected_cupcakes = 0
        self.spawn_timer = 0
        self.spawn_delay = CUPCAKE_SPAWN_DELAY
        self.character_speed = CHARACTER_SPEED
        self.is_active = False

    def toggle(self, character_position=None):
        self.is_active = not self.is_active
        if not self.is_active:
            self.reset()
            if character_position:
                character_position.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        return self.is_active

    def update(self, dt, character_position, character_rect):
        if not self.is_active:
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

        # Keep character within screen bounds
        character_position.x = max(0, min(character_position.x, SCREEN_WIDTH - character_rect.width))
        character_position.y = max(0, min(character_position.y, SCREEN_HEIGHT - character_rect.height))

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self._spawn_cupcake()
            self.spawn_timer = 0

        for cupcake in self.cupcakes[:]:
            if character_rect.colliderect(cupcake.rect):
                self.cupcakes.remove(cupcake)
                self.collected_cupcakes += 1

    def _spawn_cupcake(self):
        margin = 50
        width = 60
        height = int(width * (466/348))
        cupcake_size = (width, height)
        x = randint(margin, SCREEN_WIDTH - margin - cupcake_size[0])
        y = randint(margin, SCREEN_HEIGHT - margin - cupcake_size[1])
        cupcake = FunctionalAsset("assets/cupcake.png", cupcake_size, (x, y))
        self.cupcakes.append(cupcake)

    def draw(self, screen, font):
        if not self.is_active:
            return

        for cupcake in self.cupcakes:
            cupcake.draw(screen)

        counter_text = f"Cupcakes: {self.collected_cupcakes}"
        counter_surface = font.render(counter_text, True, Colors.DARK_VIOLET_BUTTON.value)
        screen.blit(counter_surface, (SCREEN_WIDTH - counter_surface.get_width() - 20, 20))

    def reset(self):
        self.cupcakes.clear()
        self.collected_cupcakes = 0
        self.spawn_timer = 0
        self.is_active = False 