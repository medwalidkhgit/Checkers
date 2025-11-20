import pygame

WIDTH, HEIGHT = 1280,720
ROWS, COLS = 8, 8
SQUARE_SIZE = 75

# rgb
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
WHITE = (255, 255, 255)

BOARD_DARK = (181, 136, 99)
BOARD_LIGHT = (240, 217, 181)

PIECE_DARK = BLACK
PIECE_LIGHT = RED

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
