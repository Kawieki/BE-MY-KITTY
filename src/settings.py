"""
Moduł zawierający globalne stałe i parametry konfiguracyjne gry.

Stałe:
    SCREEN_WIDTH (int): Szerokość ekranu gry.
    SCREEN_HEIGHT (int): Wysokość ekranu gry.
    FPS (int): Liczba klatek na sekundę.
    FOOD_COOLDOWN_DURATION (int): Czas odnowienia karmienia w milisekundach.
    AGE_INTERVAL (int): Interwał czasu zwiększania wieku w milisekundach.
    CUPCAKE_SPAWN_DELAY (int): Opóźnienie pojawienia się babeczki w milisekundach.
    CHARACTER_SPEED (float): Prędkość poruszania się postaci.
    MOUSE_PROXIMITY_THRESHOLD (int): Próg bliskości myszy w pikselach.
    ANIMAL_SCALE_FACTOR (float): Współczynnik skalowania zwierzęcia.
    PLAYTIME_COOLDOWN_DURATION (int): Czas odnowienia trybu zabawy w milisekundach.
    FALL_SPEED (int): Prędkość opadania w pikselach na sekundę.
    SPEED_TIMER (int): Licznik czasu dla prędkości.
    SPEED_INTERVAL (int): Interwał czasu zwiększania prędkości w milisekundach.
    SPEED_INCREMENT (int): Wartość zwiększenia prędkości.

Enumy:
    Colors (Enum): Enum zawierający predefiniowane kolory używane w grze.
"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FOOD_COOLDOWN_DURATION = 90000
AGE_INTERVAL = 60000
CUPCAKE_SPAWN_DELAY = 3000
CHARACTER_SPEED = 0.5
MOUSE_PROXIMITY_THRESHOLD = 120
ANIMAL_SCALE_FACTOR = 1.5
PLAYTIME_COOLDOWN_DURATION = 30000
FALL_SPEED = 200
SPEED_TIMER = 0
SPEED_INTERVAL = 10000
SPEED_INCREMENT = 50

from enum import Enum
class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    DARK_GRAY = (40, 40, 40)
    PINK = (255, 192, 203)
    PINK_MENU = (255, 182, 193)
    BUTTON_PINK = (255, 105, 180)
    DARK_VIOLET_BUTTON = (148, 0, 211)
    KUROMI_BACKGROUND = (210, 208, 255)
    MELODY_BACKGROUND = (255, 182, 193)
    HELLOKITTY_BACKGROUND = (255, 218, 185)
    CINNAMOROLL_BACKGROUND = (230, 230, 250)
    TEXT_COLOR = (75, 0, 130)
    BROWN = (210, 180, 140)




