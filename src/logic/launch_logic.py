import pygame
from random import uniform, randint

class LaunchLogic:
    """
    Logika wystrzeliwania obiektu w grze, zarządzająca jego pozycją, prędkością oraz interakcją ze zwierzęciem.

    Atrybuty:
        screen_width (int): Szerokość ekranu gry.
        screen_height (int): Wysokość ekranu gry.
        margin (int): Margines od krawędzi ekranu, w którym obiekt odbija się.
        velocity (Vector2): Prędkość obiektu w przestrzeni 2D.
        position (Rect): Prostokąt określający pozycję obiektu.
        animal (Animal): Obiekt zwierzęcia, którego poziom znudzenia może być zmniejszany.
    """
    def __init__(self, screen_width, screen_height, margin=20):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = margin
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = None
        self.animal = None

    def set_position(self, rect):
        """
        Ustawia pozycję obiektu.

        Args:
            rect (Rect): Prostokąt określający pozycję obiektu.
        """
        self.position = rect

    def set_animal(self, animal):
        """
            Ustawia obiekt zwierzęcia.

            Args:
                animal (Animal): Obiekt zwierzęcia, którego poziom znudzenia może być zmniejszany.
            """
        self.animal = animal

    def launch(self):
        """
           Wystrzeliwuje zwierzaka z losowym kątem i prędkością.
        """
        angle = uniform(0, 360)
        speed = uniform(20, 30)
        self.velocity = pygame.math.Vector2(speed, 0).rotate(angle)

    def update(self):
        """
            Aktualizuje pozycję zwierzaka oraz obsługuje odbicia od krawędzi ekranu.

            Returns:
                tuple: Zaktualizowana pozycja (`Rect`) oraz prędkość (`Vector2`) obiektu.
        """
        if self.position is None:
            raise ValueError("Position must be set before update")
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        bounced = False

        if self.position.left <= self.margin:
            self.position.left = self.margin
            self.velocity.x *= -1
            self.velocity.rotate_ip(uniform(-20, 20))
            bounced = True
            if self.animal and self.animal.boredom_level > 0:
                reduction = uniform(0.75, 1.25)
                self.animal.boredom_level = max(0.0, self.animal.boredom_level - reduction)

        if self.position.right >= self.screen_width - self.margin:
            self.position.right = self.screen_width - self.margin
            self.velocity.x *= -1
            self.velocity.rotate_ip(uniform(-20, 20))
            bounced = True
            if self.animal and self.animal.boredom_level > 0:
                reduction = uniform(0.75, 1.25)
                self.animal.boredom_level = max(0.0, self.animal.boredom_level - reduction)

        if self.position.top <= self.margin:
            self.position.top = self.margin
            self.velocity.y *= -1
            self.velocity.rotate_ip(uniform(-20, 20))
            bounced = True
            if self.animal and self.animal.boredom_level > 0:
                reduction = uniform(0.75, 1.25)
                self.animal.boredom_level = max(0.0, self.animal.boredom_level - reduction)

        if self.position.bottom >= self.screen_height - self.margin:
            self.position.bottom = self.screen_height - self.margin
            self.velocity.y *= -1
            self.velocity.rotate_ip(uniform(-20, 20))
            bounced = True
            if self.animal and self.animal.boredom_level > 0:
                reduction = uniform(0.75, 1.25)
                self.animal.boredom_level = max(0.0, self.animal.boredom_level - reduction)

        drift = pygame.math.Vector2(uniform(-0.2, 0.2), uniform(-0.2, 0.2))
        self.velocity += drift

        if not bounced:
            self.velocity *= 0.98

        if self.velocity.length() < 0.5:
            self.velocity = pygame.math.Vector2(0, 0)

        return self.position, self.velocity

    def is_moving(self):
        """
            Sprawdza, czy zwierzak się porusza.

            Returns:
                bool: Zwraca `True`, jeśli prędkość zwierzaka jest większa niż 0.5, w przeciwnym razie `False`.
        """
        return self.velocity.length() > 0.5
