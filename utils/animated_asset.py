import os
import pygame

class AnimatedAsset:
    def __init__(self, folder, size, pos, frame_duration=100):
        self.frames = []
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.frame_duration = frame_duration
        self.pos = pos
        self.load_frames(folder, size)

    def load_frames(self, folder, size):
        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
                img = pygame.transform.scale(img, size)
                self.frames.append(img)

    def update(self, dt):
        if not self.frames:
            return
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.time_since_last_frame = 0

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
