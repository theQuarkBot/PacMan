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

FPS = 60

START_STATE = "start"
PLAYING_STATE = "playing"
GAME_OVER_STATE = "game over"

ARROW_CONTROLS = (K_UP, K_DOWN, K_LEFT, K_RIGHT)
WASD_CONTROLS = (K_w, K_s, K_a, K_d)

PACMAN_SPEED = 2
GHOST_SPEED = 2
GHOST_WEAK_SPEED = 1

GHOST_RED = (255, 0, 0, 255)          # red ghost
GHOST_PINK = (255, 128, 255, 255)     # pink ghost
GHOST_LIGHT_BLUE = (128, 255, 255, 255)  # light blue
GHOST_ORANGE = (255, 128, 0, 255)    # orange  
GHOST_WEAK = (50, 50, 255, 255)    # blue, vulnerable ghost
GHOST_WHITE = (255, 255, 255, 255)  # white, flashing ghost

BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
WALL_COLOR = (0, 0, 255)
PELLET_COLOR = (255, 255, 0)

BOARD = [
  ['o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o','o'],
  ['%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%'],
  ['%','a','a','a','a','a','a','a','a','%','a','a','a','a','a','a','a','a','%'],
  ['%','s','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','s','%'],
  ['%','a','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','a','%'],
  ['%','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','%'],
  ['%','a','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','a','%'],
  ['%','a','a','a','a','%','a','a','a','%','a','a','a','%','a','a','a','a','%'],
  ['%','%','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','%','%'],
  ['o','o','o','%','a','%','a','a','a','a','a','a','a','%','a','%','o','o','o'],
  ['%','%','%','%','a','%','a','%','%','-','%','%','a','%','a','%','%','%','%'],
  ['o','o','o','o','a','a','a','%','o','o','o','%','a','a','a','o','o','o','o'],
  ['%','%','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','%','%'],
  ['o','o','o','%','a','%','a','a','a','a','a','a','a','%','a','%','o','o','o'],
  ['%','%','%','%','a','%','a','%','%','%','%','%','a','%','a','%','%','%','%'],
  ['%','a','a','a','a','a','a','a','a','%','a','a','a','a','a','a','a','a','%'],
  ['%','a','%','%','a','%','%','%','a','%','a','%','%','%','a','%','%','a','%'],
  ['%','s','a','%','a','a','a','a','a','o','a','a','a','a','a','%','a','s','%'],
  ['%','%','a','%','a','%','a','%','%','%','%','%','a','%','a','%','a','%','%'],
  ['%','a','a','a','a','%','a','a','a','%','a','a','a','%','a','a','a','a','%'],
  ['%','a','%','%','%','%','%','%','a','%','a','%','%','%','%','%','%','a','%'],
  ['%','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','%'],
  ['%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%','%']
]

count = 0
for row in BOARD:
    for item in row:
       if item == 'a' or item == 's':
         count += 1

PELLET_NUM = count
START_LIVES = 3

BLOCKSIZE = 32
NUM_COLS = len(BOARD[0])
NUM_ROWS = len(BOARD)
WIDTH, HEIGHT = BLOCKSIZE * NUM_COLS, BLOCKSIZE * NUM_ROWS

PACMAN_START_POS = (9 * BLOCKSIZE, 17 * BLOCKSIZE)
GHOST_START_POS = (9 * BLOCKSIZE, 11 * BLOCKSIZE)