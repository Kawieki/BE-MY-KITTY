import pygame

from src.settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT

class BackgroundRenderer:
    """
    Menedżer tła gry, odpowiedzialny za rysowanie odpowiedniego tła na podstawie wybranego charakteru lub domyślnego ustawienia.

    Atrybuty:
        backgrounds (dict[str, Surface]): Słownik zawierający tła przypisane do nazw charakterów.
        default_background (Surface): Domyślne tło wyświetlane, gdy nazwa charakteru nie jest rozpoznana.
    """
    def __init__(self):
        """
            Inicjalizuje menedżer tła gry, tworząc tła dla różnych charakterów oraz domyślne tło.
        """
        self.backgrounds = {
            "kuromi": create_background(Colors.KUROMI_BACKGROUND),
            "melody": create_background(Colors.MELODY_BACKGROUND),
            "hellokitty": create_background(Colors.HELLOKITTY_BACKGROUND),
            "cinnamoroll": create_background(Colors.CINNAMOROLL_BACKGROUND)
        }
        self.default_background = create_background(Colors.WHITE)

    def draw(self, screen, character_name):
        """
            Rysuje tło na ekranie na podstawie nazwy charakteru.

            Args:
                screen (Surface): Powierzchnia ekranu, na której tło ma być narysowane.
                character_name (str): Nazwa charakteru, dla którego ma być wyświetlone tło.
        """
        background = self.backgrounds.get(character_name, self.default_background)
        screen.blit(background, (0, 0))


def create_background(color):
    """
        Tworzy powierzchnię tła o określonym kolorze.
        Args:
            color (Color): Kolor tła.
        Returns:
            Surface: Powierzchnia tła wypełniona podanym kolorem.
    """
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.fill(color.value)
    return bg