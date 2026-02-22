# game_logic.py
# Core game logic separated from terminal I/O.
# This module has NO print statements, NO input calls, and NO color codes.
# It can be used by any frontend: terminal, web, tests, etc.

import random
import math


class Board:
    """Represents a tic-tac-toe board and its rules."""

    def __init__(self):
        self.cells = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        self.move_history = []

    def reset(self):
        """Clear the board for a new game."""
        self.cells = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"]
        ]
        self.move_history = []

    def get_cell(self, row, col):
        return self.cells[row][col]

    def place_move(self, row, col, player):
        """Place a mark on the board. Returns True if successful."""
        if self.cells[row][col] in ["X", "O"]:
            return False
        self.cells[row][col] = player
        spot_number = row * 3 + col + 1
        self.move_history.append((player, spot_number))
        return True

    def is_valid_move(self, row, col):
        """Check if a position is open."""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        return self.cells[row][col] not in ["X", "O"]

    def get_open_spots(self):
        """Return list of (row, col) tuples for unoccupied cells."""
        spots = []
        for row in range(3):
            for col in range(3):
                if self.cells[row][col] not in ["X", "O"]:
                    spots.append((row, col))
        return spots

    def check_winner(self):
        """Return 'X', 'O', or None."""
        b = self.cells

        # Rows
        for row in b:
            if row[0] == row[1] == row[2]:
                return row[0]

        # Columns
        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col]:
                return b[0][col]

        # Diagonals
        if b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]

        return None

    def get_winning_line(self):
        """Return the list of (row, col) positions that form the winning line, or None."""
        b = self.cells

        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] in ["X", "O"]:
                return [(i, 0), (i, 1), (i, 2)]

        for j in range(3):
            if b[0][j] == b[1][j] == b[2][j] and b[0][j] in ["X", "O"]:
                return [(0, j), (1, j), (2, j)]

        if b[0][0] == b[1][1] == b[2][2] and b[0][0] in ["X", "O"]:
            return [(0, 0), (1, 1), (2, 2)]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] in ["X", "O"]:
            return [(0, 2), (1, 1), (2, 0)]

        return None

    def is_full(self):
        """Return True if all spots are taken."""
        for row in self.cells:
            for spot in row:
                if spot not in ["X", "O"]:
                    return False
        return True

    def is_game_over(self):
        """Return True if the game has ended (win or tie)."""
        return self.check_winner() is not None or self.is_full()

    def copy(self):
        """Return a deep copy of this board (for AI simulations)."""
        new_board = Board()
        new_board.cells = [row[:] for row in self.cells]
        new_board.move_history = self.move_history[:]
        return new_board

    @staticmethod
    def spot_to_coords(spot):
        """Convert a 1-9 spot number to (row, col)."""
        spot = int(spot) - 1
        return spot // 3, spot % 3

    @staticmethod
    def coords_to_spot(row, col):
        """Convert (row, col) to a 1-9 spot number."""
        return row * 3 + col + 1


class AI:
    """Computer opponent with multiple difficulty levels."""

    DIFFICULTIES = ["easy", "medium", "hard", "impossible"]

    def __init__(self, difficulty, mark, opponent_mark):
        if difficulty not in self.DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        self.difficulty = difficulty
        self.mark = mark
        self.opponent_mark = opponent_mark
        self.last_explanation = ""

    def get_move(self, board):
        """Pick a move and set self.last_explanation. Returns (row, col)."""
        if self.difficulty == "easy":
            return self._move_easy(board)
        elif self.difficulty == "medium":
            return self._move_medium(board)
        elif self.difficulty == "hard":
            return self._move_hard(board)
        else:
            return self._move_impossible(board)

    # --- Easy: pure random ---
    def _move_easy(self, board):
        open_spots = board.get_open_spots()
        move = random.choice(open_spots)
        self.last_explanation = "Picking a random spot"
        return move

    # --- Medium: 50% chance of optimal move, otherwise random ---
    def _move_medium(self, board):
        if random.random() < 0.5:
            move = self._move_hard(board)
            # Keep the explanation from hard mode but tag it
            return move
        else:
            move = self._move_easy(board)
            return move

    # --- Hard: priority-based heuristic (original logic) ---
    def _move_hard(self, board):
        # 1. WIN
        winning = self._find_winning_move(board, self.mark)
        if winning:
            self.last_explanation = "Going for the win!"
            return winning

        # 2. BLOCK
        blocking = self._find_winning_move(board, self.opponent_mark)
        if blocking:
            self.last_explanation = "Blocking your winning move"
            return blocking

        # 3. CENTER
        if board.is_valid_move(1, 1):
            self.last_explanation = "Taking the center"
            return (1, 1)

        # 4. CORNER
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        open_corners = [c for c in corners if board.is_valid_move(*c)]
        if open_corners:
            move = random.choice(open_corners)
            self.last_explanation = "Taking a corner"
            return move

        # 5. RANDOM
        self.last_explanation = "Taking an open spot"
        open_spots = board.get_open_spots()
        return random.choice(open_spots)

    # --- Impossible: minimax algorithm (never loses) ---
    def _move_impossible(self, board):
        best_score = -math.inf
        best_move = None

        for row, col in board.get_open_spots():
            # Try the move
            board.cells[row][col] = self.mark
            score = self._minimax(board, is_maximizing=False, depth=0)
            board.cells[row][col] = str(row * 3 + col + 1)

            if score > best_score:
                best_score = score
                best_move = (row, col)

        # Generate explanation based on what minimax found
        self._explain_impossible_move(board, best_move)
        return best_move

    def _minimax(self, board, is_maximizing, depth):
        """Minimax recursive search.

        The AI (maximizing) wants the highest score.
        The opponent (minimizing) wants the lowest score.
        +10 = AI wins, -10 = opponent wins, 0 = tie.
        Depth is subtracted/added to prefer faster wins and slower losses.
        """
        winner = board.check_winner()
        if winner == self.mark:
            return 10 - depth
        elif winner == self.opponent_mark:
            return depth - 10
        elif board.is_full():
            return 0

        if is_maximizing:
            best = -math.inf
            for row, col in board.get_open_spots():
                board.cells[row][col] = self.mark
                score = self._minimax(board, False, depth + 1)
                board.cells[row][col] = str(row * 3 + col + 1)
                best = max(best, score)
            return best
        else:
            best = math.inf
            for row, col in board.get_open_spots():
                board.cells[row][col] = self.opponent_mark
                score = self._minimax(board, True, depth + 1)
                board.cells[row][col] = str(row * 3 + col + 1)
                best = min(best, score)
            return best

    def _explain_impossible_move(self, board, move):
        """Set a human-readable explanation for the chosen move."""
        row, col = move

        # Check if it's a winning move
        board.cells[row][col] = self.mark
        if board.check_winner() == self.mark:
            board.cells[row][col] = str(row * 3 + col + 1)
            self.last_explanation = "Going for the win!"
            return
        board.cells[row][col] = str(row * 3 + col + 1)

        # Check if it's blocking
        board.cells[row][col] = self.opponent_mark
        if board.check_winner() == self.opponent_mark:
            board.cells[row][col] = str(row * 3 + col + 1)
            self.last_explanation = "Blocking your winning move"
            return
        board.cells[row][col] = str(row * 3 + col + 1)

        # Center
        if (row, col) == (1, 1):
            self.last_explanation = "Taking the center"
            return

        # Corner
        if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            self.last_explanation = "Taking a strategic corner"
            return

        self.last_explanation = "Playing the optimal move"

    @staticmethod
    def _find_winning_move(board, player):
        """Return (row, col) that wins for player, or None."""
        for row, col in board.get_open_spots():
            original = board.cells[row][col]
            board.cells[row][col] = player
            if board.check_winner() == player:
                board.cells[row][col] = original
                return (row, col)
            board.cells[row][col] = original
        return None
