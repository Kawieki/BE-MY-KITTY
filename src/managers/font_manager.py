import pygame

class FontManager:
    """
    Menedżer czcionek odpowiedzialny za ładowanie i przechowywanie czcionek w grze.

    Atrybuty:
        _fonts (dict): Słownik przechowujący załadowane czcionki, gdzie klucz to nazwa czcionki, a wartość to obiekt czcionki Pygame.
        """

    _fonts = {}

    @staticmethod
    def load_font(name, path, size):
        """
        Ładuje czcionkę z podanej ścieżki i zapisuje ją w menedżerze czcionek.

        Args:
            name (str): Nazwa czcionki, pod którą będzie przechowywana.
            path (str): Ścieżka do pliku czcionki.
            size (int): Rozmiar czcionki.

        Returns:
            None
        """
        FontManager._fonts[name] = pygame.font.Font(path, size)

    @staticmethod
    def get_font(name):
        """
        Pobiera załadowaną czcionkę na podstawie jej nazwy.

        Args:
            name (str): Nazwa czcionki do pobrania.

        Returns:
            Font: Obiekt czcionki Pygame lub `None`, jeśli czcionka o podanej nazwie nie została załadowana.
        """
        return FontManager._fonts.get(name)
