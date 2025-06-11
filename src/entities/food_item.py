import pygame

class FoodItem:
    """
    Reprezentuje element jedzenia, który można przeciągać w grze.

    Atrybuty:
        image (Surface): Obraz jedzenia wczytany z pliku.
        rect (Rect): Prostokąt określający pozycję i rozmiar obrazu jedzenia.
        dragging (bool): Flaga wskazująca, czy element jest aktualnie przeciągany.
        offset (tuple): Przesunięcie pozycji myszy względem górnego lewego rogu prostokąta
    """
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.dragging = False
        self.offset = (0, 0)

    def handle_event(self, event):
        """
            Obsługuje zdarzenia myszy, takie jak kliknięcie, przeciąganie i puszczenie.

            Args:
                event (Event): Zdarzenie Pygame, które ma być obsłużone.

            Returns:
                bool: Zwraca `True`, jeśli element został puszczony, w przeciwnym razie `False`.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mx, my = event.pos
                ox, oy = self.rect.topleft
                self.offset = (ox - mx, oy - my)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.rect.topleft = (mx + self.offset[0], my + self.offset[1])

        return False

    def draw(self, screen):
        """
           Rysuje element jedzenia na ekranie.

            Args:
                screen (Surface): Powierzchnia Pygame, na której element ma być narysowany.
        """
        screen.blit(self.image, self.rect)
