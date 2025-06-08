from random import uniform

class GameLogic:
    def __init__(self, animal, playtime):
        self.animal = animal
        self.playtime = playtime
        self.playtime_remaining = 0
        self.launch_mode = False
        self.cooldown_duration = 15000
        self.in_cooldown = False
        self.cooldown_timer = 0
        self.boredom_timer = 0
        self.hunger_timer = 0

    def toggle_launch_mode(self):
        if self.in_cooldown:
            return False
        self.launch_mode = not self.launch_mode
        if self.launch_mode:
            self.playtime_remaining = self.playtime * 1000
        else:
            self.playtime_remaining = 0
        return True

    def update(self, dt, is_moving):
        """
        Główna metoda aktualizująca logikę gry.

        :param dt: Czas, który upłynął od ostatniej aktualizacji (w milisekundach).
        :param is_moving: Flaga wskazująca, czy zwierzę się porusza.
        """
        self._update_boredom(dt)
        self._update_hunger(dt)
        self._reduce_boredom_if_moving(dt, is_moving)
        self._update_playtime(dt)
        self._update_cooldown(dt)

    def _update_boredom(self, dt):
        """
        Aktualizuje poziom znudzenia zwierzęcia co sekundę.
        """
        self.boredom_timer += dt
        if self.boredom_timer >= 1000:
            self.animal.boredom_level = min(100, self.animal.boredom_level + uniform(0.5, 0.75))
            self.boredom_timer -= 1000

    def _update_hunger(self, dt):
        """
        Aktualizuje poziom głodu zwierzęcia co sekundę.
        """
        self.hunger_timer += dt
        if self.hunger_timer >= 1000:
            self.animal.hunger_level = min(100, self.animal.hunger_level + uniform(0.20, 0.75))
            self.hunger_timer -= 1000

    def _reduce_boredom_if_moving(self, dt, is_moving):
        """
        Zmniejsza poziom znudzenia, jeśli zwierzę się porusza.
        """
        if is_moving:
            self.animal.boredom_level = max(0, self.animal.boredom_level - 0.002 * dt)

    def _update_playtime(self, dt):
        """
        Aktualizuje czas zabawy i przełącza tryb na cooldown, gdy czas się skończy.
        """
        if self.launch_mode:
            self.playtime_remaining -= dt
            if self.playtime_remaining <= 0:
                self.launch_mode = False
                self.in_cooldown = True
                self.cooldown_timer = self.cooldown_duration

    def _update_cooldown(self, dt):
        """
        Aktualizuje czas cooldownu i wyłącza go, gdy czas się skończy.
        """
        if self.in_cooldown:
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0:
                self.in_cooldown = False
                self.cooldown_timer = 0
