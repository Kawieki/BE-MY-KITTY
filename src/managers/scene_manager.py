class SceneManager:
    """
    Menedżer scen odpowiedzialny za przełączanie między scenami, obsługę zdarzeń, aktualizację logiki oraz rysowanie scen.

    Atrybuty:
        current_scene (Scene): Aktualnie aktywna scena.
    """
    def __init__(self, initial_scene):
        self.current_scene = initial_scene

    def switch_scene(self, new_scene):
        """
            Przełącza na nową scenę.

            Args:
                new_scene (Scene): Scena, na którą należy przełączyć.
        """
        self.current_scene = new_scene

    def handle_events(self, events):
        """
            Obsługuje zdarzenia w aktywnej scenie i przełącza scenę, jeśli jest to wymagane.

            Args:
                events (list): Lista zdarzeń do obsłużenia.
        """
        next_scene = self.current_scene.handle_events(events)
        if next_scene:
            self.switch_scene(next_scene)

    def update(self, dt):
        """
            Aktualizuje logikę aktywnej sceny.

            Args:
                dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        self.current_scene.update(dt)

    def draw(self, screen):
        """
            Rysuje aktywną scenę na ekranie.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
        """
        self.current_scene.draw(screen)