import pygame
from random import randint
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.functional_asset import FunctionalAsset
from settings import FOOD_COOLDOWN_DURATION
from managers.audio_manager import AudioManager

class FoodManager:
    def __init__(self, food_quantity, animal):
        self.food_quantity = food_quantity
        self.remaining_food = food_quantity
        self.feed_cooldown = 0
        self.feed_cooldown_duration = FOOD_COOLDOWN_DURATION
        self.food_item = None
        self.animal = animal
        self.hunger_decrease = 20
        self.audio_manager = AudioManager()

    def update(self, dt):
        if self.feed_cooldown > 0:
            self.feed_cooldown -= dt
            if self.feed_cooldown <= 0:
                self.feed_cooldown = 0
                self.remaining_food = self.food_quantity

    def spawn_food(self):
        if not self.food_item and self.feed_cooldown <= 0 < self.remaining_food:
            margin = 50
            food_size = (64, 64)
            x = randint(margin, SCREEN_WIDTH - margin - food_size[0])
            y = randint(margin, SCREEN_HEIGHT - margin - food_size[1])
            food_number = randint(1, 4)
            food_image_path = f"assets/food{food_number}.png"
            self.food_item = FunctionalAsset(food_image_path, food_size, (x, y), label=None)

    def handle_food_event(self, event, character_rect):
        if self.food_item:
            if self.food_item.handle_event(event):
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.food_item.rect.colliderect(character_rect):
                        self._feed_animal()
                        return True
        return False

    def _feed_animal(self):
        self.animal.hunger_level = max(0, self.animal.hunger_level - self.hunger_decrease)
        self.food_item = None
        self.remaining_food -= 1
        self.audio_manager.play_sound_effect("assets/audio/feeding_sound.mp3")
        if self.remaining_food <= 0:
            self.feed_cooldown = self.feed_cooldown_duration

    def draw(self, screen):
        if self.food_item:
            self.food_item.draw(screen)

    def reset(self):
        self.food_item = None
        self.feed_cooldown = 0
        self.remaining_food = self.food_quantity 