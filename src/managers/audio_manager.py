import pygame
import random
import os

class AudioManager:
    """
    Menedżer audio odpowiedzialny za odtwarzanie muzyki, efektów dźwiękowych

    Atrybuty:
        current_audio (str): Ścieżka do aktualnie odtwarzanego pliku audio.
        is_animation (bool): Flaga wskazująca, czy animacja zwierzęcia jest aktywna.
        sound_dir (str): Ścieżka do katalogu z efektami dźwiękowymi.
    """
    def __init__(self):
        self.current_audio = None
        self.is_animation = False
        self.sound_dir = "assets/audio/sound"
    
    def play_audio(self, file_path, animal):
        """
        Odtwarza plik audio i aktywuje animację zwierzęcia.

        Args:
            file_path (str): Ścieżka do pliku audio.
            animal (Animal): Obiekt zwierzęcia, którego animacja ma być aktywowana.
        """
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
    
    def play_random_sound(self, animal):
        """
            Odtwarza losowy plik audio z katalogu efektów dźwiękowych.

            Args:
                animal (Animal): Obiekt zwierzęcia, którego animacja ma być aktywowana.
        """
        sound_files = [f for f in os.listdir(self.sound_dir) if f.endswith('.mp3')]
        if sound_files:
            random_sound = os.path.join(self.sound_dir, random.choice(sound_files))
            self.play_audio(random_sound, animal)
    
    def play_sound_effect(self, file_path):
        """
            Odtwarza efekt dźwiękowy.

            Args:
                file_path (str): Ścieżka do pliku efektu dźwiękowego.
        """
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.play()
        except Exception as e:
            print(f"Error loading sound effect: {e}")
    
    def stop_audio(self, animal):
        """
          Zatrzymuje odtwarzanie audio i dezaktywuje animację zwierzęcia.

          Args:
              animal (Animal): Obiekt zwierzęcia, którego animacja ma być dezaktywowana.
          """
        if self.current_audio:
            pygame.mixer.music.stop()
            self.current_audio = None
            self.is_animation = False
            animal.use_static_asset()
    
    def check_audio_finished(self, animal):
        """
           Sprawdza, czy odtwarzanie audio zostało zakończone, i zatrzymuje animację zwierzęcia.

           Args:
               animal (Animal): Obiekt zwierzęcia, którego animacja ma być dezaktywowana.
           """
        if self.current_audio and not pygame.mixer.music.get_busy():
            self.stop_audio(animal) 