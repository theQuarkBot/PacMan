from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d,
)

WIDTH, HEIGHT = 600, 600
FPS = 60

START_STATE = "start"
PLAYING_STATE = "playing"
GAME_OVER_STATE = "game over"

ARROW_CONTROLS = (K_UP, K_DOWN, K_LEFT, K_RIGHT)
WASD_CONTROLS = (K_w, K_s, K_a, K_d)

PACMAN_SPEED = 2

BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)
