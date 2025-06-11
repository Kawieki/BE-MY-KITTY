import pygame

class Bar:
    """
    Klasa reprezentująca pasek postępu który może być rysowany na ekranie.

    Atrybuty:
        x (int): Pozycja X paska na ekranie.
        y (int): Pozycja Y paska na ekranie.
        width (int): Szerokość paska.
        height (int): Wysokość paska.
        color (tuple[int, int, int]): Kolor wypełnienia paska.
        border_color (tuple[int, int, int]): Kolor obramowania paska.
        max_value (int): Maksymalna wartość paska.
        current_value (int): Aktualna wartość paska.
    """

    def __init__(self, x, y, width, height, color, border_color, max_value=100):
        """
            Inicjalizuje pasek postępu z określonymi parametrami.

            Args:
                x (int): Pozycja X paska na ekranie.
                y (int): Pozycja Y paska na ekranie.
                width (int): Szerokość paska.
                height (int): Wysokość paska.
                color (tuple[int, int, int]): Kolor wypełnienia paska.
                border_color (tuple[int, int, int]): Kolor obramowania paska.
                max_value (int, optional): Maksymalna wartość paska. Domyślnie 100.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.max_value = max_value
        self.current_value = max_value

    def set_value(self, value):
        """
            Ustawia aktualną wartość paska, ograniczając ją do zakresu od 0 do maksymalnej wartości.

            Args:
                value (int): Nowa wartość paska.
        """
        self.current_value = max(0, min(value, self.max_value))

    def draw(self, screen, rounded=False):
        """
            Rysuje pasek na ekranie, wypełniając go proporcjonalnie do aktualnej wartości.

            Args:
                screen (Surface): Powierzchnia ekranu, na której pasek ma być narysowany.
                rounded (bool, optional): Określa, czy rogi paska mają być zaokrąglone. Domyślnie `False`.
        """
        if rounded:
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), border_radius=10, width=2)
        else:
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)

        fill_width = int(self.width * (self.current_value / self.max_value))
        if rounded:
            pygame.draw.rect(screen, self.color, (self.x, self.y, fill_width, self.height), border_radius=10)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, fill_width, self.height))