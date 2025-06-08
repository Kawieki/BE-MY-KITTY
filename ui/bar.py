import pygame

class Bar:
    def __init__(self, x, y, width, height, color, border_color, max_value=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.max_value = max_value
        self.current_value = max_value

    def set_value(self, value):
        """Set the current value of the bar."""
        self.current_value = max(0, min(value, self.max_value))

    def draw(self, screen, rounded=False):
        """Draw the bar on the screen."""
        # Draw the border
        if rounded:
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), border_radius=10, width=2)
        else:
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)

        # Draw the filled portion
        fill_width = int(self.width * (self.current_value / self.max_value))
        if rounded:
            pygame.draw.rect(screen, self.color, (self.x, self.y, fill_width, self.height), border_radius=10)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, fill_width, self.height))