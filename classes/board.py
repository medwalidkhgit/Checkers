import pygame
import math
from .constants import BOARD_DARK, BOARD_LIGHT, PIECE_DARK, PIECE_LIGHT, ROWS, COLS, SQUARE_SIZE, WIDTH, HEIGHT, GREY
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        # Calculate offsets for centering
        self.board_offset_x = (WIDTH - (COLS * SQUARE_SIZE)) // 2
        self.board_offset_y = (HEIGHT - (ROWS * SQUARE_SIZE)) // 2
        # Load wooden background
        self.wood_bg = pygame.image.load("assets/wood.jpeg")
        self.wood_bg = pygame.transform.scale(self.wood_bg, (COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE))
        # Initialize font for turn indicator
        self.font = pygame.font.Font("assets/ps2p.ttf", 36)
    
    def draw_turn_indicator(self, win, turn, black_time, white_time):
        # Create text for turn
        turn_text = "WHITE'S TURN" if turn == PIECE_LIGHT else "BLACK'S TURN"
        text_surface = self.font.render(turn_text, True, (255, 0, 0))  # Red color
        
        # Calculate position (centered above the board)
        text_rect = text_surface.get_rect(centerx=self.board_offset_x + (COLS * SQUARE_SIZE) // 2,
                                        top=self.board_offset_y - 50)
        
        # Draw text with a subtle shadow for better visibility
        shadow_surface = self.font.render(turn_text, True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        win.blit(shadow_surface, shadow_rect)
        win.blit(text_surface, text_rect)

        # Draw timers
        timer_font = pygame.font.Font("assets/ps2p.ttf", 28)
        
        # Black timer (extreme left)
        black_time_text = f"BLACK: {self.format_time(black_time)}"
        black_surface = timer_font.render(black_time_text, True, (0, 0, 0))
        black_rect = black_surface.get_rect(
            left=20,  # 20px from left edge
            top=self.board_offset_y + (ROWS * SQUARE_SIZE) + 20  # 20px below the board
        )
        win.blit(black_surface, black_rect)
        
        # White timer (extreme right)
        white_time_text = f"WHITE: {self.format_time(white_time)}"
        white_surface = timer_font.render(white_time_text, True, (255, 255, 255))
        white_rect = white_surface.get_rect(
            right=WIDTH - 20,  # 20px from right edge
            top=self.board_offset_y + (ROWS * SQUARE_SIZE) + 20  # 20px below the board
        )
        win.blit(white_surface, white_rect)

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def draw_squares(self, win):
        # Fill background with grey
        win.fill(GREY)
        # Draw wooden background
        win.blit(self.wood_bg, (self.board_offset_x, self.board_offset_y))
        # Draw the squares with transparency
        for row in range(ROWS):
            for col in range(COLS):
                color = BOARD_DARK if (row + col) % 2 == 0 else BOARD_LIGHT
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(s, (*color, 180), (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                win.blit(s, (col * SQUARE_SIZE + self.board_offset_x, 
                           row * SQUARE_SIZE + self.board_offset_y))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == PIECE_LIGHT:
                self.red_kings += 1
            else:
                self.white_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PIECE_LIGHT))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PIECE_DARK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win, turn, black_time, white_time):
        self.draw_squares(win)
        self.draw_turn_indicator(win, turn, black_time, white_time)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == PIECE_LIGHT:
                self.red_left -= 1
            else:
                self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return PIECE_DARK
        elif self.white_left <= 0:
            return PIECE_LIGHT
        return None
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == PIECE_DARK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == PIECE_LIGHT or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def draw_valid_moves(self, moves):
        board_offset_x = (WIDTH - (COLS * SQUARE_SIZE)) // 2
        board_offset_y = (HEIGHT - (ROWS * SQUARE_SIZE)) // 2
        
        # Enhanced animation parameters
        t = pygame.time.get_ticks() / 1000.0  # Slower animation (800ms cycle)
        base_radius = 15  # Smaller base radius
        pulse = 6 * math.sin(t)  # Smaller pulse
        glow_radius = int(base_radius + pulse)
        
        for move in moves:
            row, col = move
            center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_x
            center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + board_offset_y
            
            # # Draw outer glow
            # glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            # for r in range(glow_radius, 0, -2):
            #     alpha = int(100 * (1 - r/glow_radius))  # Fade out towards the edge
            #     pygame.draw.circle(glow_surface, (0, 0, 255, alpha), (glow_radius, glow_radius), r)
            # win.blit(glow_surface, (center_x - glow_radius, center_y - glow_radius))
            
            # # Draw inner circle
            # inner_radius = int(base_radius * 0.6)  # Smaller inner circle
            # pygame.draw.circle(win, (0, 0, 255), (center_x, center_y), inner_radius)
            
            # # Draw pulsing ring
            # ring_radius = int(base_radius + pulse * 0.4)  # Smaller ring
            # pygame.draw.circle(win, (0, 0, 255), (center_x, center_y), ring_radius, 2)

    def get_board_state(self):
        """
        Returns a serializable representation of the board state for network transmission
        """
        state = {
            "board_pieces": [],
            "red_left": self.red_left,
            "white_left": self.white_left,
            "red_kings": self.red_kings,
            "white_kings": self.white_kings
        }
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    # Store piece data in a serializable format
                    piece_data = {
                        "row": piece.row,
                        "col": piece.col,
                        "color": piece.color,
                        "king": piece.king
                    }
                    state["board_pieces"].append(piece_data)
        
        return state

    def set_board_state(self, state):
        """
        Sets the board state based on a received network state
        """
        if not state:
            return
            
        # Reset board
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 0
        
        # Set piece counts
        self.red_left = state["red_left"]
        self.white_left = state["white_left"]
        self.red_kings = state["red_kings"]
        self.white_kings = state["white_kings"]
        
        # Add pieces
        for piece_data in state["board_pieces"]:
            piece = Piece(piece_data["row"], piece_data["col"], piece_data["color"])
            if piece_data["king"]:
                piece.make_king()
            self.board[piece_data["row"]][piece_data["col"]] = piece