import pygame

class FontManager:
    _fonts = {}

    @staticmethod
    def load_font(name, path, size):
        """Load a font and store it in the font manager."""
        FontManager._fonts[name] = pygame.font.Font(path, size)

    @staticmethod
    def get_font(name):
        """Retrieve a loaded font by name."""
        return FontManager._fonts.get(name)
