class SceneManager:
    def __init__(self, initial_scene):
        self.current_scene = initial_scene

    def switch_scene(self, new_scene):
        """Przełącz na nową scenę."""
        self.current_scene = new_scene

    def handle_events(self, events):
        """Obsługa zdarzeń dla aktualnej sceny."""
        next_scene = self.current_scene.handle_events(events)
        if next_scene:  # Jeśli obecna scena zwróci nową scenę, przełącz na nią
            self.switch_scene(next_scene)

    def update(self, dt):
        """Aktualizuj aktualną scenę."""
        self.current_scene.update(dt)

    def draw(self, screen):
        """Rysuj aktualną scenę."""
        self.current_scene.draw(screen)