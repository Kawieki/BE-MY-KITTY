import pygame

class FoodItem:
    """
        Reprezentuje jedzenie w grze, które można przeciągać i upuszczać.

        Atrybuty:
            image (Surface): Obraz jedzenia.
            rect (Rect): Prostokąt określający pozycję i rozmiar jedzenia.
            dragging (bool): Flaga wskazująca, czy jedzenie jest aktualnie przeciągane.
            offset (tuple): Przesunięcie pozycji myszy względem pozycji jedzenia.
    """
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.dragging = False
        self.offset = (0, 0)

    def handle_event(self, event):
        """
            Obsługuje zdarzenia myszy związane z przeciąganiem jedzenia.

            Parametry:
                event (Event): Zdarzenie Pygame.

            Zwraca:
                bool: True, jeśli przeciąganie zostało zakończone, w przeciwnym razie False.
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
            Rysuje jedzenie na ekranie.

            Parametry:
            screen (Surface): Powierzchnia ekranu, na której jedzenie ma być narysowane.
        """
        screen.blit(self.image, self.rect)
