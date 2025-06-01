class SceneManager:
    def __init__(self, initial_scene):
        self.current_scene = initial_scene

    def set_scene(self, scene):
        self.current_scene = scene

    def get_scene(self):
        return self.current_scene