import pygame
from logic.cupcake_mode import CupcakeMode
from logic.food_manager import FoodManager
from logic.game_logic import GameLogic
from logic.launch_logic import LaunchLogic
from managers.audio_manager import AudioManager
from scenes.base_scene import BaseScene
from settings import ANIMAL_SCALE_FACTOR, MOUSE_PROXIMITY_THRESHOLD, Colors
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.background_renderer import BackgroundRenderer
from ui.game_ui import GameUI
from utils.animated_asset import AnimatedAsset


class GameScene(BaseScene):
    """
    Scena gry, obsługująca logikę rozgrywki, interakcje użytkownika oraz rysowanie elementów gry.

    Atrybuty:
        font (Font): Czcionka używana do wyświetlania tekstu.
        animal (Animal): Obiekt zwierzęcia, które jest głównym elementem gry.
        current_audio (Audio): Aktualnie odtwarzany dźwięk.
        is_animation (bool): Flaga określająca, czy animacja jest aktywna.
        background_manager (BackgroundRenderer): Menedżer tła gry.
        ui (GameUI): Interfejs użytkownika gry.
        food_manager (FoodManager): Menedżer jedzenia w grze.
        cupcake_mode (CupcakeMode): Tryb gry związany z babeczkami.
        audio_manager (AudioManager): Menedżer dźwięków w grze.
        last_click_time (int): Czas ostatniego kliknięcia myszą.
        double_click_delay (int): Maksymalny czas między kliknięciami dla podwójnego kliknięcia.
        last_click_pos (tuple): Pozycja ostatniego kliknięcia myszą.
        phone_image (Surface): Obraz telefonu wyświetlanego w grze.
        phone_rect (Rect): Prostokąt określający pozycję telefonu na ekranie.
    """
    def __init__(self, animal, food_quantity, playtime):
        """
            Inicjalizuje scenę gry, ustawiając zwierzę, ilość jedzenia, czas zabawy oraz elementy interfejsu.

            Args:
                animal (Animal): Obiekt zwierzęcia w grze.
                food_quantity (int): Ilość jedzenia dostępnego w grze.
                playtime (int): Czas zabawy w sekundach.
        """
        self.font = pygame.font.SysFont(None, 24)
        self.animal = animal
        self.current_audio = None
        self.is_animation = False
        self.animal.use_static_asset()
        self._initialize_logics(playtime)

        self.background_manager = BackgroundRenderer()
        self.ui = GameUI(self.font)
        self.food_manager = FoodManager(food_quantity, self.animal)
        self.cupcake_mode = CupcakeMode()
        self.audio_manager = AudioManager()

        self.last_click_time = 0
        self.double_click_delay = 300
        self.last_click_pos = None

        original_phone = pygame.image.load("assets/phone.png")
        new_width = 60
        new_height = int((new_width / 362) * 816)
        self.phone_image = pygame.transform.scale(original_phone, (new_width, new_height))
        self.phone_rect = self.phone_image.get_rect()
        self.phone_rect.bottomleft = (20, SCREEN_HEIGHT - 20)

    def _initialize_logics(self, playtime):
        initial_rect = self.animal.static_asset.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.launch_logic = LaunchLogic(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.launch_logic.set_position(initial_rect)
        self.launch_logic.set_animal(self.animal)
        self.game_logic = GameLogic(self.animal, playtime)

    def _is_double_click(self, mouse_pos):
        current_time = pygame.time.get_ticks()
        if self.last_click_pos and self.last_click_time:
            time_diff = current_time - self.last_click_time
            distance = pygame.math.Vector2(mouse_pos).distance_to(pygame.math.Vector2(self.last_click_pos))
            
            if time_diff < self.double_click_delay and distance < 10:
                self.last_click_time = 0
                self.last_click_pos = None
                return True
        
        self.last_click_time = current_time
        self.last_click_pos = mouse_pos
        return False

    def handle_events(self, events):
        """
            Obsługuje zdarzenia użytkownika, takie jak kliknięcia myszą, ruchy myszą, wprowadzanie klawiszy oraz przeciąganie plików.

            Args:
                events (list[Event]): Lista zdarzeń do obsłużenia.

            Returns:
                Scene: Nowa scena, jeśli użytkownik wywołał zmianę sceny, w przeciwnym razie `None`.
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if self._is_double_click(mouse_pos):
                    if self.launch_logic.position.collidepoint(mouse_pos):
                        self.audio_manager.play_random_sound(self.animal)
                        continue

                if self.phone_rect.collidepoint(mouse_pos):
                    self.audio_manager.play_audio("assets/audio/butterfly.mp3", self.animal)
                    self.is_animation = self.audio_manager.is_animation
                    continue
                
                if self.ui.cupcake_button.is_clicked(mouse_pos):
                    if not self.game_logic.in_cooldown and self.game_logic.can_enter_cupcake_mode():
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
        """
            Rysuje scenę gry, w tym tło, zwierzę, interfejs użytkownika oraz elementy gry.

            Args:
                screen (Surface): Powierzchnia ekranu, na której scena ma być narysowana.
            """
        self.background_manager.draw(screen, self.animal.static_asset.name)
        self._draw_animal(screen)
        screen.blit(self.phone_image, self.phone_rect)
        
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
                from scenes.pause_menu_scene import PauseMenuScene
                return PauseMenuScene(self)

    def _handle_drop_file(self, file_path):
        if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
            self.audio_manager.play_audio(file_path, self.animal)
            self.is_animation = self.audio_manager.is_animation

    def update(self, dt):
        """
            Aktualizuje logikę sceny gry, w tym tryb babeczek, animacje, logikę gry oraz interfejs użytkownika.

            Args:
                 dt (float): Czas, który upłynął od ostatniej aktualizacji.
        """
        if self.cupcake_mode.is_active:
            self.cupcake_mode.update(dt, self.launch_logic.position, self.launch_logic.position)
            self._update_animation(dt)
            self._update_bars()
        else:
            self._update_normal_mode(dt)

    def _update_normal_mode(self, dt):
        self._update_launch_logic()
        self._update_animation(dt)
        self._update_game_logic(dt)
        self._update_bars()
        self.audio_manager.check_audio_finished(self.animal)
        self.is_animation = self.audio_manager.is_animation
        self.food_manager.update(dt)
        self.ui.update_button_states(self.game_logic, self.food_manager.feed_cooldown)
        self._handle_mouse_proximity_during_play()

    def _update_launch_logic(self):
        pos, vel = self.launch_logic.update()
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

        food_text = f"Food left: {self.food_manager.remaining_food}"
        food_surface = self.font.render(food_text, True, Colors.WHITE.value)
        food_rect = food_surface.get_rect(midbottom=(self.ui.feed_button.rect.midtop[0], self.ui.feed_button.rect.top - 5))
        screen.blit(food_surface, food_rect)
        
        self.ui.feed_button.draw(screen)
        self.ui.cupcake_button.set_enabled(not self.game_logic.in_cooldown)
        self.ui.cupcake_button.draw(screen)
        self.food_manager.draw(screen)