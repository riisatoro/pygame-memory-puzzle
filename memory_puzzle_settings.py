TITLE = "Memory puzzle"
FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOXES_OPEN_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)
RESOLUTION = (WINDOW_WIDTH, WINDOW_HEIGHT)
REVEAL_SPEED = 8

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)


BG_COLOR = NAVYBLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE
BOARD_COLOR = GRAY

DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
OVAL = "oval"

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT