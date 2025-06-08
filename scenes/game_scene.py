import pygame
from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.base_scene import BaseScene
from ui.bar import Bar
from ui.button import Button
from logic.launch_logic import LaunchLogic
from logic.game_logic import GameLogic
from utils.animated_asset import AnimatedAsset
from random import randint
from utils.functional_asset import FunctionalAsset


def initialize_bar_positions():
    bar_width = 200
    bar_height = 20
    bar_x = 100
    hunger_bar_y = 20
    boredom_bar_y = hunger_bar_y + bar_height + 30
    return bar_x, bar_width, bar_height, hunger_bar_y, boredom_bar_y


class GameScene(BaseScene):
    def __init__(self, animal, food_quantity, playtime):
        self.font = pygame.font.SysFont(None, 24)
        self.animal = animal
        self.current_audio = None
        self.is_animation = False

        self._load_background()
        self._initialize_bars()
        self._initialize_buttons()
        self._initialize_logics(playtime)

        self.food_quantity = food_quantity
        self.remaining_food = food_quantity
        self.feed_cooldown = 0
        self.feed_cooldown_duration = 90000  # 1 min 30 s
        self.food_item = None

        self.animal.use_static_asset()

    def _load_background(self):
        self.background_image = pygame.image.load("assets/background.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def _initialize_bars(self):
        bar_x, bar_width, bar_height, hunger_bar_y, boredom_bar_y = initialize_bar_positions()
        self.hunger_bar = Bar(bar_x, hunger_bar_y, bar_width, bar_height, (210, 180, 140), Colors.WHITE.value)
        self.boredom_bar = Bar(bar_x, boredom_bar_y, bar_width, bar_height, Colors.BLUE.value, Colors.WHITE.value)

    def _initialize_buttons(self):
        button_width, button_height = 150, 40
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = SCREEN_HEIGHT - 60
        self.launch_button = Button(button_x, button_y, button_width, button_height, "Play TIME! :3", font=self.font, color=Colors.DARK_VIOLET_BUTTON.value)

        feed_x = button_x - button_width - 20
        self.feed_button = Button(feed_x, button_y, button_width, button_height, "Feed Me :3", font=self.font, color=Colors.GREEN.value)

    def _initialize_logics(self, playtime):
        initial_rect = self.animal.static_asset.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.launch_logic = LaunchLogic(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.launch_logic.set_position(initial_rect)
        self.game_logic = GameLogic(self.animal, playtime)

    def handle_events(self, events):
        for event in events:
            # Obsługa przeciągania i karmienia
            if self.food_item:
                if self.food_item.handle_event(event):
                    if self.food_item.rect.colliderect(self.launch_logic.position):
                        self.animal.hunger_level = max(0, self.animal.hunger_level - 20)
                        self.food_item = None
                        self.remaining_food -= 1
                        if self.remaining_food <= 0:
                            self.feed_cooldown = self.feed_cooldown_duration
                    continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if not self.game_logic.launch_mode and not self.game_logic.in_cooldown:
                    if self.launch_button.is_clicked(mouse_pos):
                        toggled = self.game_logic.toggle_launch_mode()
                        if toggled:
                            self.launch_button.set_enabled(False)

                # Feed logic
                if self.feed_button.is_clicked(mouse_pos):
                    if not self.food_item and self.feed_cooldown <= 0 < self.remaining_food:
                        self._spawn_food()

            elif event.type == pygame.KEYDOWN:
                if not self.game_logic.launch_mode:
                    new_scene = self._handle_keydown(event.key)
                    if new_scene:
                        return new_scene

            elif event.type == pygame.DROPFILE:
                if not self.game_logic.launch_mode:
                    self._handle_dropfile(event.file)

    def _handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self._stop_audio()
            from scenes.menu_scene import MenuScene
            return MenuScene()

    def _handle_dropfile(self, file_path):
        if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
            self._play_audio(file_path)

    def _play_audio(self, file_path):
        if self.current_audio:
            pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.current_audio = file_path
            self.is_animation = True
            self.animal.use_animated_asset()
        except Exception as e:
            print(f"Error loading audio file: {e}")

    def _stop_audio(self):
        if self.current_audio:
            pygame.mixer.music.stop()
            self.current_audio = None
            self.is_animation = False
            self.animal.use_static_asset()

    def update(self, dt):
        self._update_launch_logic(dt)
        self._update_animation(dt)
        self._update_game_logic(dt)
        self._update_bars()
        self._check_audio_finished()

        if not self.game_logic.in_cooldown and not self.game_logic.launch_mode:
            self.launch_button.set_enabled(True)
        else:
            self.launch_button.set_enabled(False)

        # Aktualizuj cooldown karmienia
        if self.feed_cooldown > 0:
            self.feed_cooldown -= dt
            if self.feed_cooldown <= 0:
                self.feed_cooldown = 0
                self.remaining_food = self.food_quantity  # resetuj jedzenie

        # Włącz/wyłącz przycisk FEED na podstawie warunków
        if self.feed_cooldown > 0 or self.game_logic.launch_mode:
            self.feed_button.set_enabled(False)
        else:
            self.feed_button.set_enabled(True)

        self._handle_mouse_proximity_during_play()

    def _handle_mouse_proximity_during_play(self):
        # Automatyczne odpalenie zabawy przy najechaniu kursorem na postać
        if self.game_logic.launch_mode and not self.launch_logic.is_moving():
            mouse_pos = pygame.mouse.get_pos()
            if self.launch_logic.position.collidepoint(mouse_pos):
                self.launch_logic.launch()

        # Uciekanie postaci od kursora
        if self.game_logic.launch_mode:
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            center_pos = pygame.math.Vector2(self.launch_logic.position.center)
            distance = mouse_pos.distance_to(center_pos)
            threshold = 120

            if distance < threshold:
                direction = center_pos - mouse_pos
                if direction.length() != 0:
                    direction = direction.normalize()
                    speed = 15
                    self.launch_logic.velocity = direction * speed

    def _update_launch_logic(self, dt):
        pos, vel = self.launch_logic.update(dt)
        self.launch_logic.set_position(pos)

    def _update_animation(self, dt):
        if self.is_animation and isinstance(self.animal.current_asset, AnimatedAsset):
            self.animal.current_asset.pos = self.launch_logic.position.topleft
            self.animal.current_asset.update(dt)

    def _update_game_logic(self, dt):
        prev_launch_mode = self.game_logic.launch_mode
        self.game_logic.update(dt, self.launch_logic.is_moving())

        if prev_launch_mode and not self.game_logic.launch_mode:
            center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.launch_logic.position.center = center_pos
            self.launch_logic.velocity = pygame.math.Vector2(0, 0)

    def _update_bars(self):
        self.hunger_bar.set_value(self.animal.hunger_level)
        self.boredom_bar.set_value(self.animal.boredom_level)

    def _check_audio_finished(self):
        if self.current_audio and not pygame.mixer.music.get_busy():
            self._stop_audio()

    def draw(self, screen):
        self._draw_background(screen)
        self._draw_animal(screen)
        self._draw_status_bars(screen)
        self._draw_animal_info(screen)
        self._draw_timer_and_status(screen)
        self.launch_button.draw(screen)
        self.feed_button.draw(screen)

        if self.food_item:
            self.food_item.draw(screen)

        self._draw_food_info_above_button(screen)

    def _draw_background(self, screen):
        screen.blit(self.background_image, (0, 0))

    def _draw_animal(self, screen):
        scale_factor = 1.5
        if self.is_animation and isinstance(self.animal.current_asset, AnimatedAsset):
            self.animal.current_asset.draw_scaled(screen, scale_factor)
        else:
            image = self.animal.current_asset.image
            w, h = image.get_size()
            new_w, new_h = int(w * scale_factor), int(h * scale_factor)
            scaled_image = pygame.transform.scale(image, (new_w, new_h))
            center = self.launch_logic.position.center
            new_rect = scaled_image.get_rect(center=center)
            screen.blit(scaled_image, new_rect)

    def _draw_status_bars(self, screen):
        hunger_label = self.font.render("Hunger", True, Colors.WHITE.value)
        screen.blit(hunger_label, (self.hunger_bar.x - 90, self.hunger_bar.y + 2))
        self.hunger_bar.draw(screen, rounded=True)

        boredom_label = self.font.render("Boredom", True, Colors.WHITE.value)
        screen.blit(boredom_label, (self.boredom_bar.x - 90, self.boredom_bar.y + 2))
        self.boredom_bar.draw(screen, rounded=True)

    def _draw_animal_info(self, screen):
        name_label = self.font.render(self.animal.name, True, Colors.WHITE.value)
        asset_x = self.launch_logic.position.centerx - name_label.get_width() // 2
        asset_y = self.launch_logic.position.bottom + 30
        screen.blit(name_label, (asset_x, asset_y))

        age_label = self.font.render(f"Age: {self.animal.age}", True, Colors.WHITE.value)
        age_rect = age_label.get_rect(center=(SCREEN_WIDTH // 2, 10))
        screen.blit(age_label, age_rect)

    def _draw_status_text(self, screen, text, color, y_offset):
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(topright=(SCREEN_WIDTH - 20, y_offset))
        screen.blit(surface, rect)
        return rect.bottom

    def _draw_timer_and_status(self, screen):
        y_offset = 20

        if self.game_logic.launch_mode:
            seconds_left = max(0, int(self.game_logic.playtime_remaining / 1000))
            timer_text = f"Time Left: {seconds_left}s"
            y_offset = self._draw_status_text(screen, timer_text, Colors.WHITE.value, y_offset)

            status_text = "Playtime mode: ON"
            status_color = Colors.GREEN.value
            y_offset = self._draw_status_text(screen, status_text, status_color, y_offset + 5)

        elif self.game_logic.in_cooldown:
            cooldown_seconds = max(0, int(self.game_logic.cooldown_timer / 1000) + 1)
            cooldown_text = f"Cooldown: {cooldown_seconds}s"
            y_offset = self._draw_status_text(screen, cooldown_text, Colors.RED.value, y_offset)

            status_text = "Playtime mode: OFF"
            status_color = Colors.RED.value
            y_offset = self._draw_status_text(screen, status_text, status_color, y_offset + 5)

        else:
            status_text = "Playtime Mode: OFF"
            status_color = Colors.RED.value
            y_offset = self._draw_status_text(screen, status_text, status_color, y_offset)

        if self.feed_cooldown > 0:
            seconds_left = max(0, int(self.feed_cooldown / 1000) + 1)
            feed_cooldown_text = f"Feed Cooldown: {seconds_left}s"
            self._draw_status_text(screen, feed_cooldown_text, Colors.RED.value, y_offset + 10)

    def _draw_food_info_above_button(self, screen):
        if self.feed_cooldown == 0:
            text = f"Food left: {self.remaining_food}"
            color = Colors.WHITE.value
            label_surface = self.font.render(text, True, color)
            label_rect = label_surface.get_rect(center=(self.feed_button.rect.centerx, self.feed_button.rect.top - 20))
            screen.blit(label_surface, label_rect)

    def _spawn_food(self):
        margin = 50
        food_size = (64, 64)
        x = randint(margin, SCREEN_WIDTH - margin - food_size[0])
        y = randint(margin, SCREEN_HEIGHT - margin - food_size[1])
        food_image_path = "assets/food.png"
        self.food_item = FunctionalAsset(food_image_path, food_size, (x, y), label=None)