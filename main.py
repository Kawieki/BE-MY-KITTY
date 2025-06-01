import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.menu_scene import MenuScene
from utils.scene_manager import SceneManager

def main():
    pygame.init()
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

        new_scene = scene_manager.get_scene().handle_events(events)
        if new_scene is not None:
            scene_manager.set_scene(new_scene)

        scene_manager.get_scene().update(dt)
        scene_manager.get_scene().draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()