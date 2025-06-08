import pygame
from settings import Colors, SCREEN_WIDTH

from ui.bar import Bar
from ui.button import Button

def initialize_bar_positions():
    bar_width = 200
    bar_height = 20
    bar_x = 100
    hunger_bar_y = 20
    boredom_bar_y = hunger_bar_y + bar_height + 30
    return bar_x, bar_width, bar_height, hunger_bar_y, boredom_bar_y

class UIManager:
    def __init__(self, font):
        bar_x, bar_width, bar_height, hunger_bar_y, boredom_bar_y = initialize_bar_positions()
        self.hunger_bar = Bar(bar_x, hunger_bar_y, bar_width, bar_height, (210, 180, 140), Colors.WHITE.value)
        self.boredom_bar = Bar(bar_x, boredom_bar_y, bar_width, bar_height, Colors.BLUE.value, Colors.WHITE.value)

        button_width, button_height = 150, 40
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = 540  # Assuming SCREEN_HEIGHT = 600; możesz dostosować

        self.launch_button = Button(button_x, button_y, button_width, button_height, "Play TIME! :3", font=font, color=Colors.DARK_VIOLET_BUTTON.value)

        feed_x = button_x - button_width - 20
        self.feed_button = Button(feed_x, button_y, button_width, button_height, "Feed Me :3", font=font, color=Colors.GREEN.value)

    def draw_status_bars(self, screen, font):
        hunger_label = font.render("Hunger", True, Colors.WHITE.value)
        screen.blit(hunger_label, (self.hunger_bar.x - 90, self.hunger_bar.y + 2))
        self.hunger_bar.draw(screen, rounded=True)

        boredom_label = font.render("Boredom", True, Colors.WHITE.value)
        screen.blit(boredom_label, (self.boredom_bar.x - 90, self.boredom_bar.y + 2))
        self.boredom_bar.draw(screen, rounded=True)

    def update_bars(self, animal):
        self.hunger_bar.set_value(animal.hunger_level)
        self.boredom_bar.set_value(animal.boredom_level)

    def draw_buttons(self, screen):
        self.launch_button.draw(screen)
        self.feed_button.draw(screen)

    def update_buttons(self, game_logic, food_manager):
        if not game_logic.in_cooldown and not game_logic.launch_mode:
            self.launch_button.set_enabled(True)
        else:
            self.launch_button.set_enabled(False)
