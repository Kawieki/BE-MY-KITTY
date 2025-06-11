import pygame
from src.utils.asset import Asset

class FunctionalAsset(Asset):
    """
    Klasa FunctionalAsset rozszerza klasę Asset, dodając funkcjonalność przeciągania zasobu za pomocą myszy.

    Atrybuty:
        rect (Rect): Prostokąt określający pozycję i rozmiar zasobu, używany do detekcji kolizji.
        dragging (bool): Flaga określająca, czy zasób jest aktualnie przeciągany.
        offset_x (int): Przesunięcie pozycji X zasobu względem kursora myszy podczas przeciągania.
        offset_y (int): Przesunięcie pozycji Y zasobu względem kursora myszy podczas przeciągania.
    """
    def __init__(self, path, size, position, label=None, font_size=24, font_color=(255, 255, 255)):
        """
               Inicjalizuje funkcjonalny zasób graficzny z możliwością przeciągania.

               Args:
                   path (str): Ścieżka do pliku graficznego zasobu.
                   size (tuple[int, int]): Rozmiar zasobu (szerokość, wysokość).
                   position (tuple[int, int]): Pozycja zasobu na ekranie (X, Y).
                   label (str, optional): Tekst etykiety wyświetlany pod zasobem. Domyślnie `None`.
                   font_size (int, optional): Rozmiar czcionki etykiety. Domyślnie 24.
                   font_color (tuple[int, int, int], optional): Kolor czcionki etykiety w formacie RGB. Domyślnie `(255, 255, 255)`.
               """
        super().__init__(path, size, position, label, font_size, font_color)
        self.rect = pygame.Rect(position, size)
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def handle_event(self, event):
        """
            Obsługuje zdarzenia myszy, takie jak kliknięcie, przeciąganie i zwolnienie zasobu.

            Args:
                 event (Event): Zdarzenie Pygame, które ma być obsłużone.

            Returns:
                bool: `True`, jeśli zdarzenie zostało obsłużone, w przeciwnym razie `False`.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
                self.position = (self.rect.x, self.rect.y)
                return True

        return False

    def draw(self, screen):
        """
            Rysuje zasób graficzny na ekranie, aktualizując jego pozycję na podstawie prostokąta.

            Args:
                screen (Surface): Powierzchnia ekranu, na której zasób ma być narysowany.
        """
        self.position = (self.rect.x, self.rect.y)
        super().draw(screen)
