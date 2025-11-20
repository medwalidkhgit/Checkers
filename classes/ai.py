import random
from .constants import ROWS, COLS, PIECE_LIGHT, PIECE_DARK

class AIPlayer:
    def __init__(self, color, difficulty="medium"):
        self.color = color
        difficulty_map = {"easy": 1, "medium": 2, "hard": 3}
        self.difficulty = difficulty_map.get(difficulty, 2)
        self.depth = {1: 3, 2: 5, 3: 7}[self.difficulty]

    def evaluate_board(self, board):
        score = 0
        capture_opportunities = 0
        opponent_color = PIECE_LIGHT if self.color == PIECE_DARK else PIECE_DARK

        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece == 0:
                    continue

                mod = 1 if piece.color == self.color else -1
                score += mod * 10
                if piece.king:
                    score += mod * 30

                # Positional bonuses
                if row in (3, 4) and col in (3, 4):
                    score += mod * 5
                if col in (0, 7):
                    score += mod * 3
                if (piece.color == PIECE_DARK and row == 0) or (piece.color == PIECE_LIGHT and row == 7):
                    score += mod * 10

                if piece.color == self.color:
                    moves = board.get_valid_moves(piece)
                    for skipped in moves.values():
                        if skipped:
                            capture_opportunities += len(skipped) * 15

        score += capture_opportunities
        return score

    def get_all_moves(self, game, color=None):
        color = color or self.color
        valid_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = game.board.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    moves = game.board.get_valid_moves(piece)
                    for move, skipped in moves.items():
                        valid_moves.append(((row, col), move, skipped))
        valid_moves.sort(key=lambda x: len(x[2]), reverse=True)
        return valid_moves

    def simulate_move(self, game, piece_pos, move, skipped):
        piece = game.board.get_piece(*piece_pos)
        original_row, original_col = piece.row, piece.col
        was_king = piece.king

        game.board.move(piece, *move)
        if skipped:
            game.board.remove(skipped)

        # Handle promotion
        if move[0] == 0 or move[0] == ROWS - 1:
            piece.make_king()
            if piece.color == PIECE_LIGHT:
                game.board.red_kings += 1
            else:
                game.board.white_kings += 1

        return piece, (original_row, original_col), was_king, skipped

    def undo_move(self, game, piece, old_pos, was_king, skipped):
        game.board.move(piece, *old_pos)
        if not was_king:
            piece.king = False
            if piece.color == PIECE_LIGHT:
                game.board.red_kings -= 1
            else:
                game.board.white_kings -= 1

        if skipped:
            for s in skipped:
                game.board.board[s.row][s.col] = s
                if s.color == PIECE_LIGHT:
                    game.board.red_left += 1
                else:
                    game.board.white_left += 1

    def minimax(self, game, depth, alpha, beta, maximizing):
        if depth == 0 or game.winner() is not None:
            return self.evaluate_board(game.board), None

        color = self.color if maximizing else (PIECE_LIGHT if self.color == PIECE_DARK else PIECE_DARK)
        valid_moves = self.get_all_moves(game, color)
        if not valid_moves:
            return self.evaluate_board(game.board), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for piece_pos, move, skipped in valid_moves:
                piece, old_pos, was_king, skip_data = self.simulate_move(game, piece_pos, move, skipped)
                eval_score, _ = self.minimax(game, depth - 1, alpha, beta, False)
                self.undo_move(game, piece, old_pos, was_king, skip_data)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (piece_pos, move)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for piece_pos, move, skipped in valid_moves:
                piece, old_pos, was_king, skip_data = self.simulate_move(game, piece_pos, move, skipped)
                eval_score, _ = self.minimax(game, depth - 1, alpha, beta, True)
                self.undo_move(game, piece, old_pos, was_king, skip_data)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (piece_pos, move)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def make_move(self, game):
        valid_moves = self.get_all_moves(game)
        if not valid_moves:
            return False

        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        if best_move is None:
            piece_pos, move, _ = random.choice(valid_moves)
        else:
            piece_pos, move = best_move

        game.select(*piece_pos)
        game.select(*move)
        return True
