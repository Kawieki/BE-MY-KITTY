class BaseScene:
    """
    Podstawowa klasa sceny, definiująca interfejs dla obsługi zdarzeń, aktualizacji logiki oraz rysowania.
    """
    def handle_events(self, events):
        """
            Obsługuje zdarzenia przekazane do sceny.

            Args:
                events (list): Lista zdarzeń do obsłużenia.
        """
        pass

    def update(self, dt):
        """
            Aktualizuje logikę sceny.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        pass

    def draw(self, screen):
        """
            Rysuje scenę na ekranie.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
        """
        pass