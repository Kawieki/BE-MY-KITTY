import os
import pygame

class AnimatedAsset:
    """
    Klasa reprezentująca animowana grafike, która może być rysowana na ekranie.

    Atrybuty:
        folder (str): Ścieżka do folderu zawierającego pliki klatek animacji.
        size (tuple[int, int]): Rozmiar każdej klatki animacji (szerokość, wysokość).
        pos (tuple[int, int]): Pozycja zasobu na ekranie (X, Y).
        frames (list[Surface]): Lista klatek animacji.
        current_frame (int): Indeks aktualnie wyświetlanej klatki animacji.
        animation_speed (int): Prędkość animacji w milisekundach.
        animation_timer (int): Licznik czasu animacji.
    """
    def __init__(self, folder, size, pos):
        """
            Inicjalizuje animacje.

            Args:
                folder (str): Ścieżka do folderu zawierającego pliki klatek animacji.
                size (tuple[int, int]): Rozmiar każdej klatki animacji (szerokość, wysokość).
                pos (tuple[int, int]): Pozycja zasobu na ekranie (X, Y).
        """
        self.folder = folder
        self.size = size
        self.pos = pos
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 60
        self.animation_timer = 0
        self._load_frames()

    def _load_frames(self):
        """
            Ładuje klatki animacji z folderu.

            Raises:
                Exception: W przypadku błędu podczas ładowania klatek animacji.
            """
        try:
            frame_files = sorted([f for f in os.listdir(self.folder) if f.endswith('.png')])
            for frame_file in frame_files:
                frame_path = os.path.join(self.folder, frame_file)
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, self.size)
                self.frames.append(frame)
        except Exception as e:
            print(f"Error loading animation frames: {e}")

    def update(self, dt):
        """
            Aktualizuje stan animacji na podstawie upływu czasu.

            Args:
                dt (int): Czas, który upłynął od ostatniej aktualizacji w milisekundach.
            """
        if len(self.frames) > 1:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        """
            Rysuje aktualną klatkę animacji na ekranie.

            Args:
                screen (Surface): Powierzchnia ekranu, na której klatka ma być narysowana.
        """
        if self.frames:
            screen.blit(self.frames[self.current_frame], self.pos)

    def draw_scaled(self, screen, scale_factor):
        """
            Rysuje aktualną klatkę animacji na ekranie, skalując ją o podany współczynnik.

            Args:
                screen (Surface): Powierzchnia ekranu, na której klatka ma być narysowana.
                scale_factor (float): Współczynnik skalowania klatki.
        """
        if not self.frames:
            return

        frame = self.frames[self.current_frame]
        w, h = frame.get_size()
        new_size = (int(w * scale_factor), int(h * scale_factor))
        scaled_frame = pygame.transform.scale(frame, new_size)

        rect = scaled_frame.get_rect()
        rect.topleft = self.pos
        screen.blit(scaled_frame, rect)
