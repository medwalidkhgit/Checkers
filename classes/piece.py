import pygame
from .constants import PIECE_DARK, PIECE_LIGHT, SQUARE_SIZE, GREY, CROWN, WHITE, WIDTH, HEIGHT

BLACK_PIECE_IMG = pygame.transform.scale(pygame.image.load("assets/black_piece.png"), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
WHITE_PIECE_IMG = pygame.transform.scale(pygame.image.load("assets/white_piece.png"), (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (32, 18))



class Piece:
    PADDING = 15
    OUTLINE = 4

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        # Calculate offsets for centering
        self.board_offset_x = (WIDTH - (8 * SQUARE_SIZE)) // 2
        self.board_offset_y = (HEIGHT - (8 * SQUARE_SIZE)) // 2
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 + self.board_offset_x
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2 + self.board_offset_y

    def make_king(self):
        self.king = True

    # def draw(self, win):
    #     radius = SQUARE_SIZE // 2 - self.PADDING
    #     outline_color = WHITE
        
    #     pygame.draw.circle(win, outline_color, (self.x, self.y), radius + self.OUTLINE)
    #     pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    #     if self.king:
    #         win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))
    def draw(self, win):
        if self.color == PIECE_DARK:  # black player
            image = BLACK_PIECE_IMG
        else:  # red player (using white piece image)
            image = WHITE_PIECE_IMG

        rect = image.get_rect(center=(self.x, self.y))
        win.blit(image, rect)

        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)