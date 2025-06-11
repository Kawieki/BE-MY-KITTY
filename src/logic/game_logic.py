from random import uniform
from src.settings import AGE_INTERVAL
from src.settings import PLAYTIME_COOLDOWN_DURATION


class GameLogic:
    """
    Logika gry, zarządzająca stanem zwierzęcia, czasem zabawy oraz trybem gry.

    Atrybuty:
        animal (Animal): Obiekt zwierzęcia, którego stan jest zarządzany.
        playtime (float): Czas zabawy w milisekundach.
        playtime_remaining (float): Pozostały czas zabawy w milisekundach.
        cooldown_duration (float): Czas trwania okresu odnowienia po zabawie.
        age_interval (float): Interwał czasu, po którym zwierzę się starzeje.
        launch_mode (bool): Flaga wskazująca, czy tryb zabawy jest aktywny.
        in_cooldown (bool): Flaga wskazująca, czy okres odnowienia jest aktywny.
        cooldown_timer (float): Timer kontrolujący czas pozostały do zakończenia okresu odnowienia.
        age_timer (float): Timer kontrolujący czas do starzenia się zwierzęcia.
        boredom_timer (float): Timer kontrolujący wzrost poziomu znudzenia zwierzęcia.
        hunger_timer (float): Timer kontrolujący wzrost poziomu głodu zwierzęcia.
    """
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
        """
            Przełącza tryb zabawy.

            Returns:
                bool: Zwraca `True`, jeśli tryb zabawy został włączony, w przeciwnym razie `False`.
        """
        if not self.in_cooldown:
            self.launch_mode = not self.launch_mode
            if self.launch_mode:
                self.playtime_remaining = self.playtime * 1000
            return self.launch_mode
        return False

    def can_enter_cupcake_mode(self):
        """
            Sprawdza, czy można wejść w tryb "Cupcake Mode".

            Returns:
                bool: Zwraca `True`, jeśli tryb "Cupcake Mode" jest dostępny, w przeciwnym razie `False`.
            """
        return not self.launch_mode and not self.in_cooldown

    def update(self, dt, is_moving):
        """
            Aktualizuje stan gry.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
                is_moving (bool): Flaga wskazująca, czy postać gracza się porusza.
        """
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
        """
            Aktualizuje poziom znudzenia zwierzęcia.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        self.boredom_timer += dt
        if self.boredom_timer >= 1000:
            self.animal.boredom_level = min(100, self.animal.boredom_level + uniform(0.25, 1.25))
            self.boredom_timer = 0

    def _update_hunger(self, dt):
        """
            Aktualizuje poziom głodu zwierzęcia.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        self.hunger_timer += dt
        if self.hunger_timer >= 1000:
            self.animal.hunger_level = min(100, self.animal.hunger_level + uniform(0.25, 1.25))
            self.hunger_timer = 0

    def _reduce_boredom_if_moving(self, dt, is_moving):
        """
            Redukuje poziom znudzenia zwierzęcia, jeśli postać gracza się porusza.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
                is_moving (bool): Flaga wskazująca, czy postać gracza się porusza.
        """
        if is_moving:
            self.animal.boredom_level = max(0, self.animal.boredom_level - 0.2 * dt / 1000)

    def _update_playtime(self, dt):
        """
            Aktualizuje czas zabawy zwierzęcia.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        self.playtime_remaining -= dt
        if self.playtime_remaining <= 0:
            self.launch_mode = False
            self.in_cooldown = True
            self.cooldown_timer = self.cooldown_duration

    def _update_cooldown(self, dt):
        """
            Aktualizuje czas odnowienia po zabawie.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        self.cooldown_timer -= dt
        if self.cooldown_timer <= 0:
            self.in_cooldown = False
            self.cooldown_timer = 0

    def _update_age(self, dt):
        """
            Aktualizuje wiek zwierzęcia.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        self.age_timer += dt
        if self.age_timer >= self.age_interval:
            self.animal.age += 1
            self.age_timer = 0
