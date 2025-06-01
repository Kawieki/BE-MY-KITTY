import pygame
from entities.Animal import Animal
from scenes.base_scene import BaseScene
from scenes.game_scene import GameScene
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT

class CharacterSettingsScene(BaseScene):
    def __init__(self, selected_character):
        self.selected_character = selected_character
        self.font = pygame.font.SysFont(None, 48)
        self.title = self.font.render(self.selected_character.label, True, Colors.WHITE.value)

        self.character_data = {
            "Name": "",
            "Age": 0,
            "Hunger": 0,
            "Boredom": 0,
        }

        self.input_boxes = {
            key: pygame.Rect(SCREEN_WIDTH // 2 - 100, 200 + i * 60, 200, 40)
            for i, key in enumerate(self.character_data.keys())
        }
        self.active_box = None
        self.user_inputs = {key: value for key, value in self.character_data.items()}

        from ui.button import Button

        # Buttons for age adjustment
        self.age_up_button = Button(SCREEN_WIDTH // 2 + 110, 260, 40, 40, "+", font_size=32, color=Colors.GREEN.value)
        self.age_down_button = Button(self.age_up_button.rect.x + self.age_up_button.rect.width + 10, 260, 40, 40, "-",font_size=32, color=Colors.RED.value)

        # Buttons for Hunger
        self.hunger_up_button = Button(SCREEN_WIDTH // 2 + 110, 320, 40, 40, "+", font_size=32,color=Colors.GREEN.value)
        self.hunger_down_button = Button(self.hunger_up_button.rect.x + self.hunger_up_button.rect.width + 10, 320, 40,40, "-", font_size=32, color=Colors.RED.value)

        # Buttons for Boredom
        self.boredom_up_button = Button(SCREEN_WIDTH // 2 + 110, 380, 40, 40, "+", font_size=32,color=Colors.GREEN.value)
        self.boredom_down_button = Button(self.boredom_up_button.rect.x + self.boredom_up_button.rect.width + 10, 380,40, 40, "-", font_size=32, color=Colors.RED.value)

        self.play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Play")

        # Flags for button holding
        self.holding_flags = {
            "age_up": False,
            "age_down": False,
            "hunger_up": False,
            "hunger_down": False,
            "boredom_up": False,
            "boredom_down": False,
        }

        # Timers for button holding
        self.hold_timer = {
            "age_up": 0,
            "age_down": 0,
            "hunger_up": 0,
            "hunger_down": 0,
            "boredom_up": 0,
            "boredom_down": 0,
        }
        self.hold_delay = 100  # Delay in milliseconds

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_boxes["Name"].collidepoint(event.pos):
                    self.active_box = "Name"
                else:
                    self.active_box = None
                mouse_pos = event.pos

                if self.play_button.is_clicked(mouse_pos):

                    animal = Animal(
                        name=self.user_inputs["Name"],
                        age=self.character_data["Age"],
                        hunger_level=self.character_data["Hunger"],
                        boredom_level=self.character_data["Boredom"],
                    )
                    return GameScene(animal)

                if self.age_up_button.is_clicked(event.pos):
                    self.holding_flags["age_up"] = True
                elif self.age_down_button.is_clicked(event.pos):
                    self.holding_flags["age_down"] = True
                elif self.hunger_up_button.is_clicked(event.pos):
                    self.holding_flags["hunger_up"] = True
                elif self.hunger_down_button.is_clicked(event.pos):
                    self.holding_flags["hunger_down"] = True
                elif self.boredom_up_button.is_clicked(event.pos):
                    self.holding_flags["boredom_up"] = True
                elif self.boredom_down_button.is_clicked(event.pos):
                    self.holding_flags["boredom_down"] = True
                elif self.input_boxes["Name"].collidepoint(event.pos):
                    self.active_box = "Name"
                else:
                    self.active_box = None

            elif event.type == pygame.MOUSEBUTTONUP:
                for key in self.holding_flags:
                    self.holding_flags[key] = False

            elif event.type == pygame.KEYDOWN and self.active_box == "Name":
                if event.key == pygame.K_RETURN:
                    self.active_box = None
                elif event.key == pygame.K_BACKSPACE:
                    self.user_inputs["Name"] = self.user_inputs["Name"][:-1]
                elif len(self.user_inputs["Name"]) < 10:  # Limit input to 15 characters
                    self.user_inputs["Name"] += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.play_button.is_clicked(mouse_pos):
                    # Create an Animal object and pass it to the GameScene
                    animal = Animal(
                        name=self.character_data["Name"],
                        age=self.character_data["Age"],
                        hunger_level=self.character_data["Hunger"],
                        boredom_level=self.character_data["Boredom"],
                    )
                    return GameScene(animal)

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        for key, flag in self.holding_flags.items():
            if flag and current_time - self.hold_timer[key] >= self.hold_delay:
                if key == "age_up":
                    self.character_data["Age"] += 1
                elif key == "age_down":
                    self.character_data["Age"] = max(0, self.character_data["Age"] - 1)
                elif key == "hunger_up":
                    self.character_data["Hunger"] = min(100, self.character_data["Hunger"] + 1)
                elif key == "hunger_down":
                    self.character_data["Hunger"] = max(0, self.character_data["Hunger"] - 1)
                elif key == "boredom_up":
                    self.character_data["Boredom"] = min(100, self.character_data["Boredom"] + 1)
                elif key == "boredom_down":
                    self.character_data["Boredom"] = max(0, self.character_data["Boredom"] - 1)
                self.hold_timer[key] = current_time

    def draw(self, screen):
        screen.fill(Colors.DARK_GRAY.value)
        screen.blit(self.title, (SCREEN_WIDTH // 2 - self.title.get_width() // 2, 10))

        # Draw the selected character above the "Name" input field
        name_box = self.input_boxes["Name"]
        character_x = SCREEN_WIDTH // 2 - self.selected_character.image.get_width() // 2
        character_y = name_box.y - self.selected_character.image.get_height() - 10
        screen.blit(self.selected_character.image, (character_x, character_y))

        for key, box in self.input_boxes.items():
            # Draw labels
            label_surface = self.font.render(key + ":", True, Colors.WHITE.value)
            screen.blit(label_surface, (box.x - label_surface.get_width() - 10, box.y + 5))

            # Draw input boxes
            pygame.draw.rect(screen, Colors.BLUE.value if key == self.active_box else Colors.WHITE.value, box, 2)

            # Render the correct text for the input box
            text_surface = self.font.render(
                self.user_inputs[key] if key == "Name" else str(self.character_data[key]),
                True,
                Colors.WHITE.value
            )
            screen.blit(text_surface, (box.x + 5, box.y + 5))

        # Draw buttons
        self.age_up_button.draw(screen)
        self.age_down_button.draw(screen)
        self.hunger_up_button.draw(screen)
        self.hunger_down_button.draw(screen)
        self.boredom_up_button.draw(screen)
        self.boredom_down_button.draw(screen)
        self.play_button.draw(screen)
