import pygame

class AudioManager:
    def __init__(self):
        self.current_audio = None
        self.is_animation = False

    def play_audio(self, file_path, animal):
        if self.current_audio:
            pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.current_audio = file_path
            self.is_animation = True
            animal.use_animated_asset()
        except Exception as e:
            print(f"Error loading audio file: {e}")

    def stop_audio(self, animal):
        if self.current_audio:
            pygame.mixer.music.stop()
            self.current_audio = None
            self.is_animation = False
            animal.use_static_asset()

    def check_audio_finished(self, animal):
        if self.current_audio and not pygame.mixer.music.get_busy():
            self.stop_audio(animal) 