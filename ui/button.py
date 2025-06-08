import pygame
from settings import Colors

class Button:
    """
    Klasa reprezentująca przycisk w grze

    Atrybuty klasowe:
        x_offset (int): Poziome przesunięcie przycisku.
        y_offset (int): Pionowe przesunięcie przycisku.

    Atrybuty instancji:
        rect (pygame.Rect): Prostokąt definiujący pozycję i rozmiar przycisku.
        label (str): Tekst wyświetlany na przycisku.
        font (pygame.font.Font): Czcionka używana do tekstu przycisku.
        text_surface (pygame.Surface): Renderowana powierzchnia tekstu.
        bg_color (tuple): Kolor tła przycisku.
        x (int): Współrzędna x lewego górnego rogu przycisku.
        y (int): Współrzędna y lewego górnego rogu przycisku.
        enabled (bool): Czy przycisk jest aktywny/klikalny.

    Metody:
        draw(screen):
            Rysuje przycisk na podanym ekranie.

        is_clicked(mouse_pos):
            Sprawdza, czy przycisk został kliknięty na podstawie pozycji myszy.

        set_enabled(enabled):
            Ustawia czy przycisk jest aktywny.
    """

    x_offset = 0
    y_offset = 60

    def __init__(self, x, y, width, height, label, font=None, font_size=48, color=Colors.BLUE.value):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = font or pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(label, True, Colors.WHITE.value)
        self.bg_color = color
        self.x = x
        self.y = y
        self.enabled = True

    def set_enabled(self, enabled):
        self.enabled = enabled

    def draw(self, screen):
        # Jeśli przycisk wyłączony, zmień kolor tła i tekstu na szary
        bg_color = self.bg_color if self.enabled else (100, 100, 100)
        text_color = Colors.WHITE.value if self.enabled else (180, 180, 180)

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        # Renderuj tekst dynamicznie, aby zmienić kolor w zależności od stanu
        text_surface = self.font.render(self.label, True, text_color)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, mouse_pos):
        # Kliknięcie działa tylko, gdy przycisk jest włączony
        return self.enabled and self.rect.collidepoint(mouse_pos)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)