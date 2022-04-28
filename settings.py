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

BLOCKSIZE = 32
NUM_COLS = 19
NUM_ROWS = 22
WIDTH, HEIGHT = BLOCKSIZE * NUM_COLS, BLOCKSIZE * NUM_ROWS

PACMAN_START_POS = (9 * BLOCKSIZE, 17 * BLOCKSIZE)
GHOST_START_POS = (9 * BLOCKSIZE, 11 * BLOCKSIZE)

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
WALL_COLOR = (0, 0, 255)
PELLET_COLOR = (255, 255, 0)

MAX_SCORE = 203
START_LIVES = 3

BOARD = [
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%'],
  ['%','s','a','a','a','a','a','a','a','%','a','a','a','a','a','a','a','s','%'],
  ['%','a','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','a','%'],
  ['%','a','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','a','%'],
  ['%','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','%'],
  ['%','a','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','a','%'],
  ['%','a','a','a','s','%','a','a','a','%','a','a','a','%','s','a','a','a','%'],
  ['%','%','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','%','%'],
  ['o','o','o','%','a','%','a','a','a','a','a','a','a','%','a','%','o','o','o'],
  ['%','%','%','%','a','%','a','%','%','-','%','%','a','%','a','%','%','%','%'],
  ['o','o','o','o','a','a','a','%','o','o','o','%','a','a','a','o','o','o','o'],
  ['%','%','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','%','%'],
  ['o','o','o','%','a','%','a','a','a','a','a','a','a','%','a','%','o','o','o'],
  ['%','%','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','%','%'],
  ['%','a','a','a','s','%','a','a','a','a','a','a','a','%','s','a','a','a','%'],
  ['%','a','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','a','%'],
  ['%','a','a','a','a','a','a','a','a','o','a','a','a','a','a','a','a','a','%'],
  ['%','a','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','a','%'],
  ['%','a','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','a','%'],
  ['%','s','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','s','%'],
  ['%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%']
]