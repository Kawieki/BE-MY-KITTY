import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.menu_scene import MenuScene
from utils.scene_manager import SceneManager
from utils.font_manager import FontManager

def load_fonts():
    FontManager.load_font("Boldins", "assets/fonts/Boldins.ttf", 35)


def main():
    pygame.init()
    load_fonts()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Be My Kitty!")
    clock = pygame.time.Clock()

    scene_manager = SceneManager(MenuScene())

    running = True
    while running:
        dt = clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        scene_manager.handle_events(events)
        scene_manager.update(dt)
        scene_manager.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()