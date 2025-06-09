import pygame

from settings import Colors, SCREEN_WIDTH, SCREEN_HEIGHT


def create_background(color):
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.fill(color.value)
    return bg


class BackgroundRenderer:
    def __init__(self):
        self.backgrounds = {
            "kuromi": create_background(Colors.KUROMI_BACKGROUND),
            "melody": create_background(Colors.MELODY_BACKGROUND),
            "hellokitty": create_background(Colors.HELLOKITTY_BACKGROUND),
            "cinnamoroll": create_background(Colors.CINNAMOROLL_BACKGROUND)
        }
        self.default_background = create_background(Colors.WHITE)

    def draw(self, screen, character_name):
        background = self.backgrounds.get(character_name, self.default_background)
        screen.blit(background, (0, 0))
