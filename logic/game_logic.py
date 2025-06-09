import pygame
from random import uniform

from settings import AGE_INTERVAL
from settings import PLAYTIME_COOLDOWN_DURATION


class GameLogic:
    def __init__(self, animal, playtime):
        self.animal = animal
        self.playtime = playtime
        self.playtime_remaining = playtime
        self.cooldown_duration = PLAYTIME_COOLDOWN_DURATION
        self.age_interval = AGE_INTERVAL
        self.launch_mode = False
        self.in_cooldown = False
        self.cooldown_timer = 0
        self.age_timer = 0
        self.boredom_timer = 0
        self.hunger_timer = 0
        self.animal.hunger_level = 0
        self.animal.boredom_level = 0

    def toggle_launch_mode(self):
        if not self.in_cooldown:
            self.launch_mode = not self.launch_mode
            if self.launch_mode:
                self.playtime_remaining = self.playtime * 1000
            return self.launch_mode
        return False

    def can_enter_cupcake_mode(self):
        return not self.launch_mode and not self.in_cooldown

    def update(self, dt, is_moving):
        if self.launch_mode:
            self._update_playtime(dt)
        elif self.in_cooldown:
            self._update_cooldown(dt)
            self._update_boredom(dt)
            self._update_hunger(dt)
        else:
            self._update_boredom(dt)
            self._update_hunger(dt)
            self._reduce_boredom_if_moving(dt, is_moving)
            self._update_age(dt)

    def _update_boredom(self, dt):
        self.boredom_timer += dt
        if self.boredom_timer >= 1000:
            self.animal.boredom_level = min(100, self.animal.boredom_level + uniform(0.25, 1.25))
            self.boredom_timer = 0

    def _update_hunger(self, dt):
        self.hunger_timer += dt
        if self.hunger_timer >= 1000:
            self.animal.hunger_level = min(100, self.animal.hunger_level + uniform(0.25, 1.25))
            self.hunger_timer = 0

    def _reduce_boredom_if_moving(self, dt, is_moving):
        if is_moving:
            self.animal.boredom_level = max(0, self.animal.boredom_level - 0.2 * dt / 1000)

    def _update_playtime(self, dt):
        self.playtime_remaining -= dt
        if self.playtime_remaining <= 0:
            self.launch_mode = False
            self.in_cooldown = True
            self.cooldown_timer = self.cooldown_duration

    def _update_cooldown(self, dt):
        self.cooldown_timer -= dt
        if self.cooldown_timer <= 0:
            self.in_cooldown = False
            self.cooldown_timer = 0

    def _update_age(self, dt):
        self.age_timer += dt
        if self.age_timer >= self.age_interval:
            self.animal.age += 1
            self.age_timer = 0
