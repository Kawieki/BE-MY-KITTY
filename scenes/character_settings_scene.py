import pygame
from entities.Animal import Animal
from scenes.base_scene import BaseScene
from scenes.game_scene import GameScene
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.button import Button
from utils.animated_asset import AnimatedAsset


def format_time(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}m {secs}s"


class CharacterSettingsScene(BaseScene):
    def __init__(self, selected_character):
        self.selected_character = selected_character
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font.render(self.selected_character.label, True, Colors.WHITE.value)

        self.character_data = {
            "Name": "",
            "Age": 0,
            "Food": 1,
            "Playtime": 5,
        }

        self.input_boxes = {
            key: pygame.Rect(SCREEN_WIDTH // 2 - 100, 200 + i * 60, 200, 40)
            for i, key in enumerate(self.character_data.keys())
        }
        self.active_box = None
        self.user_inputs = {key: value for key, value in self.character_data.items()}

        # Przyciski do regulacji wartości
        self.age_up_button = Button(SCREEN_WIDTH // 2 + 110, 260, 40, 40, "+", font_size=32, color=Colors.GREEN.value)
        self.age_down_button = Button(self.age_up_button.rect.x + self.age_up_button.rect.width + 10, 260, 40, 40, "-", font_size=32, color=Colors.RED.value)

        self.food_up_button = Button(SCREEN_WIDTH // 2 + 110, 320, 40, 40, "+", font_size=32, color=Colors.GREEN.value)
        self.food_down_button = Button(self.food_up_button.rect.x + self.food_up_button.rect.width + 10, 320, 40, 40, "-", font_size=32, color=Colors.RED.value)

        self.playtime_up_button = Button(SCREEN_WIDTH // 2 + 110, 380, 40, 40, "+", font_size=32, color=Colors.GREEN.value)
        self.playtime_down_button = Button(self.playtime_up_button.rect.x + self.playtime_up_button.rect.width + 10, 380, 40, 40, "-", font_size=32, color=Colors.RED.value)

        self.play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Play")

        # Flagi trzymania przycisków
        self.holding_flags = {
            "age_up": False,
            "age_down": False,
            "food_up": False,
            "food_down": False,
            "playtime_up": False,
            "playtime_down": False,
        }

        # Timery dla trzymania przycisków
        self.hold_timer = {key: 0 for key in self.holding_flags}
        self.hold_delay = 100  # opóźnienie w ms

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if self.input_boxes["Name"].collidepoint(mouse_pos):
                    self.active_box = "Name"
                else:
                    self.active_box = None

                if self.play_button.is_clicked(mouse_pos):
                    animated_asset = AnimatedAsset(
                        folder=f"assets/characters/{self.selected_character.name}_frames",
                        size=(self.selected_character.image.get_width(), self.selected_character.image.get_height()),
                        pos=(SCREEN_WIDTH // 2 - self.selected_character.image.get_width() // 2,
                             SCREEN_HEIGHT // 2 - self.selected_character.image.get_height() // 2)
                    )
                    animal = Animal(
                        name=self.user_inputs["Name"],
                        age=self.character_data["Age"],
                        static_asset=self.selected_character,
                        animated_asset=animated_asset
                    )
                    return GameScene(animal, self.character_data["Food"], self.character_data["Playtime"])

                if self.age_up_button.is_clicked(mouse_pos):
                    self.holding_flags["age_up"] = True
                elif self.age_down_button.is_clicked(mouse_pos):
                    self.holding_flags["age_down"] = True
                elif self.food_up_button.is_clicked(mouse_pos):
                    self.holding_flags["food_up"] = True
                elif self.food_down_button.is_clicked(mouse_pos):
                    self.holding_flags["food_down"] = True
                elif self.playtime_up_button.is_clicked(mouse_pos):
                    self.holding_flags["playtime_up"] = True
                elif self.playtime_down_button.is_clicked(mouse_pos):
                    self.holding_flags["playtime_down"] = True

            elif event.type == pygame.MOUSEBUTTONUP:
                for key in self.holding_flags:
                    self.holding_flags[key] = False

            elif event.type == pygame.KEYDOWN and self.active_box == "Name":
                if event.key == pygame.K_RETURN:
                    self.active_box = None
                elif event.key == pygame.K_BACKSPACE:
                    self.user_inputs["Name"] = self.user_inputs["Name"][:-1]
                elif len(self.user_inputs["Name"]) < 10:
                    self.user_inputs["Name"] += event.unicode

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        for key, flag in self.holding_flags.items():
            if flag and current_time - self.hold_timer[key] >= self.hold_delay:
                if key == "age_up":
                    self.character_data["Age"] += 1
                elif key == "age_down":
                    self.character_data["Age"] = max(0, self.character_data["Age"] - 1)
                elif key == "food_up":
                    self.character_data["Food"] = min(100, self.character_data["Food"] + 1)
                elif key == "food_down":
                    self.character_data["Food"] = max(1, self.character_data["Food"] - 1)
                elif key == "playtime_up":
                    self.character_data["Playtime"] = min(180, self.character_data["Playtime"] + 1)
                elif key == "playtime_down":
                    self.character_data["Playtime"] = max(5, self.character_data["Playtime"] - 1)  # Minimum 5 seconds
                self.hold_timer[key] = current_time
    def draw(self, screen):
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 10))

        # Rysuj postać nad polem Name
        name_box = self.input_boxes["Name"]
        character_x = SCREEN_WIDTH // 2 - self.selected_character.image.get_width() // 2
        character_y = name_box.y - self.selected_character.image.get_height() - 10
        screen.blit(self.selected_character.image, (character_x, character_y))

        for key, box in self.input_boxes.items():
            label_surface = self.font.render(key + ":", True, Colors.WHITE.value)
            screen.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + 5))

            pygame.draw.rect(screen, Colors.BLUE.value if key == self.active_box else Colors.WHITE.value, box, 2)

            if key == "Name":
                display_text = self.user_inputs[key]
            elif key == "Food":
                display_text = f"{self.character_data[key]} units"
            elif key == "Playtime":
                display_text = format_time(self.character_data[key])
            else:
                display_text = str(self.character_data[key])

            text_surface = self.font.render(display_text, True, Colors.WHITE.value)
            screen.blit(text_surface, (box.x + 5, box.y + 5))

        # Rysowanie przycisków
        self.age_up_button.draw(screen)
        self.age_down_button.draw(screen)
        self.food_up_button.draw(screen)
        self.food_down_button.draw(screen)
        self.playtime_up_button.draw(screen)
        self.playtime_down_button.draw(screen)
        self.play_button.draw(screen)
