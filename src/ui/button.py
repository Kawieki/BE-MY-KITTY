import pygame
from settings import Colors

class Button:
    """
    Klasa reprezentująca przycisk interfejsu użytkownika, który może być rysowany na ekranie i reagować na interakcje użytkownika.

    Atrybuty:
        rect (Rect): Prostokąt określający pozycję i rozmiar przycisku.
        label (str): Tekst wyświetlany na przycisku.
        font (Font): Czcionka używana do renderowania tekstu na przycisku.
        text_surface (Surface): Powierzchnia zawierająca wyrenderowany tekst przycisku.
        bg_color (tuple[int, int, int]): Kolor tła przycisku.
        x (int): Pozycja X przycisku na ekranie.
        y (int): Pozycja Y przycisku na ekranie.
        enabled (bool): Określa, czy przycisk jest aktywny i reaguje na interakcje.
    """

    x_offset = 0
    y_offset = 60

    def __init__(self, x, y, width, height, label, font=None, font_size=48, color=Colors.BLUE.value):
        """
            Inicjalizuje przycisk interfejsu użytkownika z określonymi parametrami.

            Args:
                x (int): Pozycja X przycisku na ekranie.
                y (int): Pozycja Y przycisku na ekranie.
                width (int): Szerokość przycisku.
                height (int): Wysokość przycisku.
                label (str): Tekst wyświetlany na przycisku.
                font (Font, optional): Czcionka używana do renderowania tekstu na przycisku. Domyślnie `None`.
                font_size (int, optional): Rozmiar czcionki. Domyślnie 48.
                color (tuple[int, int, int], optional): Kolor tła przycisku. Domyślnie `Colors.BLUE.value`.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = font or pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(label, True, Colors.WHITE.value)
        self.bg_color = color
        self.x = x
        self.y = y
        self.enabled = True

    def set_enabled(self, enabled):
        """
            Ustawia stan aktywności przycisku.

            Args:
                enabled (bool): Określa, czy przycisk ma być aktywny.
        """
        self.enabled = enabled

    def draw(self, screen):
        """
            Rysuje przycisk na ekranie, uwzględniając jego stan aktywności.

            Args:
                screen (Surface): Powierzchnia ekranu, na której przycisk ma być narysowany.
         """
        bg_color = self.bg_color if self.enabled else (100, 100, 100)
        text_color = Colors.WHITE.value if self.enabled else (180, 180, 180)

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.label, True, text_color)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, mouse_pos):
        """
            Sprawdza, czy przycisk został kliknięty.

            Args:
                mouse_pos (tuple[int, int]): Pozycja kursora myszy.

            Returns:
                 bool: `True`, jeśli przycisk został kliknięty, w przeciwnym razie `False`.
        """
        return self.enabled and self.rect.collidepoint(mouse_pos)

    def is_hovered(self, mouse_pos):
        """
            Sprawdza, czy kursor myszy znajduje się nad przyciskiem.

            Args:
                mouse_pos (tuple[int, int]): Pozycja kursora myszy.

            Returns:
                 bool: `True`, jeśli kursor znajduje się nad przyciskiem, w przeciwnym razie `False`.
        """
        return self.rect.collidepoint(mouse_pos)