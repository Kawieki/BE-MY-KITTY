import os
import pygame

class AnimatedAsset:
    def __init__(self, folder, size, pos):
        self.folder = folder
        self.size = size
        self.pos = pos
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 60
        self.animation_timer = 0
        self._load_frames()

    def _load_frames(self):
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
        if len(self.frames) > 1:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        if self.frames:
            screen.blit(self.frames[self.current_frame], self.pos)

    def draw_scaled(self, screen, scale_factor):
        if not self.frames:
            return

        frame = self.frames[self.current_frame]
        w, h = frame.get_size()
        new_size = (int(w * scale_factor), int(h * scale_factor))
        scaled_frame = pygame.transform.scale(frame, new_size)

        rect = scaled_frame.get_rect()
        rect.topleft = self.pos
        screen.blit(scaled_frame, rect)

    def save_to_file(self, filepath):
        with open(filepath, "w") as f:
            f.write(f"folder={self.folder}\n")
            f.write(f"size={self.size[0]},{self.size[1]}\n")
            f.write(f"pos={self.pos[0]},{self.pos[1]}\n")
            f.write(f"animation_speed={self.animation_speed}\n")
