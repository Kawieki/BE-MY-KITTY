import pygame

class FoodItem:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.dragging = False
        self.offset = (0, 0)  

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mx, my = event.pos
                ox, oy = self.rect.topleft
                self.offset = (ox - mx, oy - my)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True  

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.rect.topleft = (mx + self.offset[0], my + self.offset[1])

        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
