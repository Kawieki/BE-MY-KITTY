import pygame

from logic.cupcake_mode import CupcakeMode
from logic.food_manager import FoodManager
from logic.game_logic import GameLogic
from logic.launch_logic import LaunchLogic
from managers.audio_manager import AudioManager
from scenes.base_scene import BaseScene
from settings import ANIMAL_SCALE_FACTOR, MOUSE_PROXIMITY_THRESHOLD
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.background_renderer import BackgroundRenderer
from ui.game_ui import GameUI
from utils.animated_asset import AnimatedAsset


class GameScene(BaseScene):
    def __init__(self, animal, food_quantity, playtime):
        self.font = pygame.font.SysFont(None, 24)
        self.animal = animal
        self.current_audio = None
        self.is_animation = False
        self.background_manager = BackgroundRenderer()
        self.animal.use_static_asset()
        self.ui = GameUI(self.font)
        self._initialize_logics(playtime)
        self.food_manager = FoodManager(food_quantity, self.animal)
        self.cupcake_mode = CupcakeMode()
        self.audio_manager = AudioManager()

    def _initialize_logics(self, playtime):
        initial_rect = self.animal.static_asset.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.launch_logic = LaunchLogic(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.launch_logic.set_position(initial_rect)
        self.launch_logic.set_animal(self.animal)
        self.game_logic = GameLogic(self.animal, playtime)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if self.ui.cupcake_button.is_clicked(mouse_pos):
                    if self.game_logic.can_enter_cupcake_mode():
                        if self.cupcake_mode.toggle(self.launch_logic.position):
                            if self.is_animation and isinstance(self.animal.current_asset, AnimatedAsset):
                                self.animal.current_asset.pos = self.launch_logic.position.topleft
                    continue

                if not self.cupcake_mode.is_active:
                    if self.food_manager.handle_food_event(event, self.launch_logic.position):
                        continue

                    if not self.game_logic.launch_mode and not self.game_logic.in_cooldown:
                        if self.ui.launch_button.is_clicked(mouse_pos):
                            if self.game_logic.toggle_launch_mode():
                                self.ui.launch_button.set_enabled(False)

                    if self.ui.feed_button.is_clicked(mouse_pos):
                        self.food_manager.spawn_food()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.food_manager.food_item:
                    self.food_manager.handle_food_event(event, self.launch_logic.position)

            elif event.type == pygame.MOUSEMOTION:
                if self.food_manager.food_item:
                    self.food_manager.food_item.handle_event(event)

            elif event.type == pygame.KEYDOWN:
                if not self.game_logic.launch_mode:
                    new_scene = self._handle_keydown(event.key)
                    if new_scene:
                        return new_scene

            elif event.type == pygame.DROPFILE:
                if not self.game_logic.launch_mode:
                    self._handle_drop_file(event.file)

    def draw(self, screen):
        self.background_manager.draw(screen, self.animal.static_asset.name)
        self._draw_animal(screen)
        if self.cupcake_mode.is_active:
            self.cupcake_mode.draw(screen, self.font)
            self.ui.cupcake_button.draw(screen)
        else:
            self._draw_normal_mode(screen)

    def _handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            if self.cupcake_mode.is_active:
                self.cupcake_mode.toggle(self.launch_logic.position)
            else:
                self.audio_manager.stop_audio(self.animal)
                from scenes.menu_scene import MenuScene
                return MenuScene()

    def _handle_drop_file(self, file_path):
        if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
            self.audio_manager.play_audio(file_path, self.animal)
            self.is_animation = self.audio_manager.is_animation

    def update(self, dt):
        if self.cupcake_mode.is_active:
            self.cupcake_mode.update(dt, self.launch_logic.position, self.launch_logic.position)
            self._update_animation(dt)
            self._update_bars()
        else:
            self._update_normal_mode(dt)

    def _update_normal_mode(self, dt):
        self._update_launch_logic(dt)
        self._update_animation(dt)
        self._update_game_logic(dt)
        self._update_bars()
        self.audio_manager.check_audio_finished(self.animal)
        self.is_animation = self.audio_manager.is_animation
        self.food_manager.update(dt)
        self.ui.update_button_states(self.game_logic, self.food_manager.feed_cooldown)
        self._handle_mouse_proximity_during_play()

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
        self.ui.hunger_bar.set_value(self.animal.hunger_level)
        self.ui.boredom_bar.set_value(self.animal.boredom_level)

    def _handle_mouse_proximity_during_play(self):
        if self.game_logic.launch_mode and not self.launch_logic.is_moving():
            mouse_pos = pygame.mouse.get_pos()
            if self.launch_logic.position.collidepoint(mouse_pos):
                self.launch_logic.launch()

        if self.game_logic.launch_mode:
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            center_pos = pygame.math.Vector2(self.launch_logic.position.center)
            distance = mouse_pos.distance_to(center_pos)

            if distance < MOUSE_PROXIMITY_THRESHOLD:
                direction = center_pos - mouse_pos
                if direction.length() != 0:
                    direction = direction.normalize()
                    speed = 15
                    self.launch_logic.velocity = direction * speed

    def _draw_animal(self, screen):
        if self.is_animation and isinstance(self.animal.current_asset, AnimatedAsset):
            self.animal.current_asset.draw_scaled(screen, ANIMAL_SCALE_FACTOR)
        else:
            if hasattr(self.animal.current_asset, 'image'):
                image = self.animal.current_asset.image
                w, h = image.get_size()
                new_w, new_h = int(w * ANIMAL_SCALE_FACTOR), int(h * ANIMAL_SCALE_FACTOR)
                scaled_image = pygame.transform.scale(image, (new_w, new_h))
                center = self.launch_logic.position.center
                new_rect = scaled_image.get_rect(center=center)
                screen.blit(scaled_image, new_rect)
            else:
                self.animal.current_asset.draw_scaled(screen, ANIMAL_SCALE_FACTOR)

    def _draw_normal_mode(self, screen):
        self.ui.draw_status_bars(screen)
        self.ui.draw_animal_info(screen, self.animal.name, self.animal.age, self.launch_logic.position)
        self.ui.draw_timer_and_status(screen, self.game_logic, self.food_manager.feed_cooldown)
        self.ui.launch_button.draw(screen)
        self.ui.feed_button.draw(screen)
        self.ui.cupcake_button.draw(screen)
        self.food_manager.draw(screen)