import pygame

class Asset:
    """
            Klasa reprezentująca asset, który może być rysowany na ekranie, opcjonalnie z etykietą tekstową.

            Atrybuty:
                path (str): Ścieżka do pliku graficznego zasobu.
                size (tuple[int, int]): Rozmiar zasobu (szerokość, wysokość).
                position (tuple[int, int]): Pozycja zasobu na ekranie (X, Y).
                label (str, optional): Tekst etykiety wyświetlany pod zasobem. Domyślnie `None`.
                name (str, optional): Nazwa zasobu, generowana na podstawie etykiety. Domyślnie `None`.
                font_size (int): Rozmiar czcionki etykiety. Domyślnie 24.
                font_color (tuple[int, int, int]): Kolor czcionki etykiety w formacie RGB. Domyślnie `(255, 255, 255)`.
                image (Surface): Powierzchnia graficzna zasobu.
                label_surface (Surface, optional): Powierzchnia graficzna etykiety. Domyślnie `None`.
                label_position (tuple[int, int], optional): Pozycja etykiety na ekranie. Domyślnie `None`.
        """
    def __init__(self, path, size, position, label=None, font_size=24, font_color=(255, 255, 255)):
        """
            Inicjalizuje zasób graficzny z opcjonalną etykietą tekstową.

            Args:
                path (str): Ścieżka do pliku graficznego zasobu.
                size (tuple[int, int]): Rozmiar zasobu (szerokość, wysokość).
                position (tuple[int, int]): Pozycja zasobu na ekranie (X, Y).
                label (str, optional): Tekst etykiety wyświetlany pod zasobem. Domyślnie `None`.
                font_size (int, optional): Rozmiar czcionki etykiety. Domyślnie 24.
                font_color (tuple[int, int, int], optional): Kolor czcionki etykiety w formacie RGB. Domyślnie `(255, 255, 255)`.
        """
        self.path = path
        self.size = size
        self.position = position
        self.label = label
        self.name = label.lower().replace(" ", "") if label else None
        self.font_size = font_size
        self.font_color = font_color

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size)

        self.label_surface = None
        self.label_position = None

    def initialize_label(self):
        """
           Inicjalizuje etykietę tekstową dla zasobu, jeśli nie została wcześniej utworzona.
        """
        if self.label and not self.label_surface:
            font = pygame.font.SysFont(None, self.font_size)
            self.label_surface = font.render(self.label, True, self.font_color)
            self.label_position = (
                self.position[0] + self.image.get_width() // 2 - self.label_surface.get_width() // 2,
                self.position[1] + self.image.get_height() + 5
            )

    def draw(self, screen):
        """
            Rysuje zasób graficzny na ekranie, a jeśli istnieje etykieta, rysuje również etykietę.

            Args:
                screen (Surface): Powierzchnia ekranu, na której zasób ma być narysowany.
        """
        screen.blit(self.image, self.position)
        if self.label:
            self.initialize_label()
            screen.blit(self.label_surface, self.label_position)
