class SceneManager:
    def __init__(self, initial_scene):
        self.current_scene = initial_scene

    def switch_scene(self, new_scene):
        self.current_scene = new_scene

    def handle_events(self, events):
        next_scene = self.current_scene.handle_events(events)
        if next_scene:
            self.switch_scene(next_scene)

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self, screen):
        self.current_scene.draw(screen)