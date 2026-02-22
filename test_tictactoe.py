# test_tictactoe.py
# Unit tests for tic-tac-toe game logic.
# Run with:  python -m pytest test_tictactoe.py -v

import os
import tempfile
from game_logic import Board, AI, GameStats, GameConfig, Tournament


# ===========================
# --- Board Tests ---
# ===========================

class TestBoard:
    def test_new_board_has_numbers(self):
        board = Board()
        assert board.get_cell(0, 0) == "1"
        assert board.get_cell(1, 1) == "5"
        assert board.get_cell(2, 2) == "9"

    def test_place_move(self):
        board = Board()
        assert board.place_move(0, 0, "X") is True
        assert board.get_cell(0, 0) == "X"

    def test_place_move_on_occupied_spot_fails(self):
        board = Board()
        board.place_move(0, 0, "X")
        assert board.place_move(0, 0, "O") is False

    def test_is_valid_move(self):
        board = Board()
        assert board.is_valid_move(0, 0) is True
        board.place_move(0, 0, "X")
        assert board.is_valid_move(0, 0) is False

    def test_is_valid_move_out_of_bounds(self):
        board = Board()
        assert board.is_valid_move(-1, 0) is False
        assert board.is_valid_move(0, 3) is False
        assert board.is_valid_move(3, 3) is False

    def test_get_open_spots(self):
        board = Board()
        assert len(board.get_open_spots()) == 9
        board.place_move(0, 0, "X")
        spots = board.get_open_spots()
        assert len(spots) == 8
        assert (0, 0) not in spots

    def test_reset(self):
        board = Board()
        board.place_move(0, 0, "X")
        board.reset()
        assert board.get_cell(0, 0) == "1"
        assert len(board.get_open_spots()) == 9

    def test_spot_to_coords(self):
        assert Board.spot_to_coords("1") == (0, 0)
        assert Board.spot_to_coords("5") == (1, 1)
        assert Board.spot_to_coords("9") == (2, 2)

    def test_coords_to_spot(self):
        assert Board.coords_to_spot(0, 0) == 1
        assert Board.coords_to_spot(1, 1) == 5
        assert Board.coords_to_spot(2, 2) == 9

    def test_copy(self):
        board = Board()
        board.place_move(0, 0, "X")
        copy = board.copy()
        copy.place_move(1, 1, "O")
        # Original should be unchanged
        assert board.get_cell(1, 1) == "5"
        assert copy.get_cell(1, 1) == "O"


# ===========================
# --- Win Detection Tests ---
# ===========================

class TestWinDetection:
    def test_no_winner_empty_board(self):
        board = Board()
        assert board.check_winner() is None

    def test_horizontal_win_row_0(self):
        board = Board()
        for col in range(3):
            board.place_move(0, col, "X")
        assert board.check_winner() == "X"

    def test_horizontal_win_row_1(self):
        board = Board()
        for col in range(3):
            board.place_move(1, col, "O")
        assert board.check_winner() == "O"

    def test_horizontal_win_row_2(self):
        board = Board()
        for col in range(3):
            board.place_move(2, col, "X")
        assert board.check_winner() == "X"

    def test_vertical_win_col_0(self):
        board = Board()
        for row in range(3):
            board.place_move(row, 0, "O")
        assert board.check_winner() == "O"

    def test_vertical_win_col_1(self):
        board = Board()
        for row in range(3):
            board.place_move(row, 1, "X")
        assert board.check_winner() == "X"

    def test_vertical_win_col_2(self):
        board = Board()
        for row in range(3):
            board.place_move(row, 2, "O")
        assert board.check_winner() == "O"

    def test_diagonal_top_left_to_bottom_right(self):
        board = Board()
        board.place_move(0, 0, "X")
        board.place_move(1, 1, "X")
        board.place_move(2, 2, "X")
        assert board.check_winner() == "X"

    def test_diagonal_top_right_to_bottom_left(self):
        board = Board()
        board.place_move(0, 2, "O")
        board.place_move(1, 1, "O")
        board.place_move(2, 0, "O")
        assert board.check_winner() == "O"

    def test_no_winner_in_progress(self):
        board = Board()
        board.place_move(0, 0, "X")
        board.place_move(0, 1, "O")
        board.place_move(1, 1, "X")
        assert board.check_winner() is None


# ===========================
# --- Winning Line Tests ---
# ===========================

class TestWinningLine:
    def test_no_winning_line_when_no_winner(self):
        board = Board()
        assert board.get_winning_line() is None

    def test_horizontal_winning_line(self):
        board = Board()
        for col in range(3):
            board.place_move(1, col, "X")
        assert board.get_winning_line() == [(1, 0), (1, 1), (1, 2)]

    def test_vertical_winning_line(self):
        board = Board()
        for row in range(3):
            board.place_move(row, 2, "O")
        assert board.get_winning_line() == [(0, 2), (1, 2), (2, 2)]

    def test_diagonal_winning_line(self):
        board = Board()
        board.place_move(0, 0, "X")
        board.place_move(1, 1, "X")
        board.place_move(2, 2, "X")
        assert board.get_winning_line() == [(0, 0), (1, 1), (2, 2)]


# ===========================
# --- Tie Detection Tests ---
# ===========================

class TestTieDetection:
    def test_not_full_at_start(self):
        board = Board()
        assert board.is_full() is False

    def test_full_board(self):
        board = Board()
        # Fill the board with a tie pattern:
        # X O X
        # X X O
        # O X O
        moves = [
            (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
            (1, 0, "X"), (1, 1, "X"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "X"), (2, 2, "O"),
        ]
        for r, c, p in moves:
            board.place_move(r, c, p)
        assert board.is_full() is True

    def test_is_game_over_on_win(self):
        board = Board()
        for col in range(3):
            board.place_move(0, col, "X")
        assert board.is_game_over() is True

    def test_is_game_over_on_tie(self):
        board = Board()
        moves = [
            (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
            (1, 0, "X"), (1, 1, "X"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "X"), (2, 2, "O"),
        ]
        for r, c, p in moves:
            board.place_move(r, c, p)
        assert board.is_game_over() is True

    def test_not_game_over_midgame(self):
        board = Board()
        board.place_move(0, 0, "X")
        assert board.is_game_over() is False


# ===========================
# --- AI Tests ---
# ===========================

class TestAIEasy:
    def test_returns_valid_move(self):
        board = Board()
        ai = AI("easy", "O", "X")
        row, col = ai.get_move(board)
        assert board.is_valid_move(row, col)

    def test_sets_explanation(self):
        board = Board()
        ai = AI("easy", "O", "X")
        ai.get_move(board)
        assert ai.last_explanation != ""


class TestAIMedium:
    def test_returns_valid_move(self):
        board = Board()
        ai = AI("medium", "O", "X")
        row, col = ai.get_move(board)
        assert board.is_valid_move(row, col)


class TestAIHard:
    def test_takes_winning_move(self):
        """Hard AI should win immediately when it can."""
        board = Board()
        board.place_move(0, 0, "O")
        board.place_move(0, 1, "O")
        # O can win at (0, 2)
        ai = AI("hard", "O", "X")
        move = ai.get_move(board)
        assert move == (0, 2)
        assert "win" in ai.last_explanation.lower()

    def test_blocks_opponent_win(self):
        """Hard AI should block the opponent's winning move."""
        board = Board()
        board.place_move(0, 0, "X")
        board.place_move(0, 1, "X")
        # X can win at (0, 2) — AI should block
        ai = AI("hard", "O", "X")
        move = ai.get_move(board)
        assert move == (0, 2)
        assert "block" in ai.last_explanation.lower()

    def test_takes_center(self):
        """Hard AI should prefer the center when no win/block needed."""
        board = Board()
        board.place_move(0, 0, "X")  # X takes a corner
        ai = AI("hard", "O", "X")
        move = ai.get_move(board)
        assert move == (1, 1)
        assert "center" in ai.last_explanation.lower()

    def test_explanation_set(self):
        board = Board()
        ai = AI("hard", "O", "X")
        ai.get_move(board)
        assert ai.last_explanation != ""


class TestAIImpossible:
    def test_takes_winning_move(self):
        """Impossible AI should win immediately when it can."""
        board = Board()
        board.place_move(0, 0, "O")
        board.place_move(0, 1, "O")
        ai = AI("impossible", "O", "X")
        move = ai.get_move(board)
        assert move == (0, 2)

    def test_blocks_opponent_win(self):
        """Impossible AI should block the opponent's winning move."""
        board = Board()
        board.place_move(0, 0, "X")
        board.place_move(0, 1, "X")
        ai = AI("impossible", "O", "X")
        move = ai.get_move(board)
        assert move == (0, 2)

    def test_never_loses_going_second(self):
        """Play many games with X random, O impossible. O should never lose."""
        import random
        random.seed(42)

        losses = 0
        for _ in range(50):
            board = Board()
            ai = AI("impossible", "O", "X")
            current = "X"
            for turn in range(9):
                if current == "X":
                    spots = board.get_open_spots()
                    row, col = random.choice(spots)
                else:
                    row, col = ai.get_move(board)
                board.place_move(row, col, current)
                winner = board.check_winner()
                if winner:
                    if winner == "X":
                        losses += 1
                    break
                current = "O" if current == "X" else "X"
        assert losses == 0, f"Impossible AI lost {losses} out of 50 games"

    def test_never_loses_going_first(self):
        """Play many games with O impossible going first, X random. O never loses."""
        import random
        random.seed(99)

        losses = 0
        for _ in range(50):
            board = Board()
            ai = AI("impossible", "O", "X")
            current = "O"
            for turn in range(9):
                if current == "X":
                    spots = board.get_open_spots()
                    row, col = random.choice(spots)
                else:
                    row, col = ai.get_move(board)
                board.place_move(row, col, current)
                winner = board.check_winner()
                if winner:
                    if winner == "X":
                        losses += 1
                    break
                current = "O" if current == "X" else "X"
        assert losses == 0, f"Impossible AI lost {losses} out of 50 games"

    def test_explanation_set(self):
        board = Board()
        ai = AI("impossible", "O", "X")
        ai.get_move(board)
        assert ai.last_explanation != ""


class TestAIInvalidDifficulty:
    def test_raises_on_unknown_difficulty(self):
        import pytest
        with pytest.raises(ValueError):
            AI("extreme", "O", "X")


# ===========================
# --- GameStats Tests ---
# ===========================

class TestGameStats:
    def _make_stats(self):
        """Create a GameStats with a temp file that auto-cleans up."""
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(path)  # start fresh
        return GameStats(filepath=path), path

    def test_new_stats_empty(self):
        stats, path = self._make_stats()
        assert stats.get_total_games() == 0
        assert stats.get_single_player_stats() == {}
        if os.path.exists(path):
            os.unlink(path)

    def test_record_single_player_win(self):
        stats, path = self._make_stats()
        stats.record_game("1", "easy", "X")
        sp = stats.get_single_player_stats()
        assert sp["easy"]["wins"] == 1
        assert sp["easy"]["losses"] == 0
        assert stats.get_total_games() == 1
        os.unlink(path)

    def test_record_single_player_loss(self):
        stats, path = self._make_stats()
        stats.record_game("1", "hard", "O")
        sp = stats.get_single_player_stats()
        assert sp["hard"]["losses"] == 1
        os.unlink(path)

    def test_record_single_player_tie(self):
        stats, path = self._make_stats()
        stats.record_game("1", "impossible", None)
        sp = stats.get_single_player_stats()
        assert sp["impossible"]["ties"] == 1
        os.unlink(path)

    def test_record_two_player(self):
        stats, path = self._make_stats()
        stats.record_game("2", None, "X")
        stats.record_game("2", None, "O")
        stats.record_game("2", None, None)
        tp = stats.get_two_player_stats()
        assert tp["wins_x"] == 1
        assert tp["wins_o"] == 1
        assert tp["ties"] == 1
        assert stats.get_total_games() == 3
        os.unlink(path)

    def test_persistence_across_loads(self):
        stats, path = self._make_stats()
        stats.record_game("1", "easy", "X")
        stats.record_game("1", "easy", "O")
        # Load from same file
        stats2 = GameStats(filepath=path)
        sp = stats2.get_single_player_stats()
        assert sp["easy"]["wins"] == 1
        assert sp["easy"]["losses"] == 1
        assert stats2.get_total_games() == 2
        os.unlink(path)

    def test_multiple_difficulties(self):
        stats, path = self._make_stats()
        stats.record_game("1", "easy", "X")
        stats.record_game("1", "hard", "X")
        stats.record_game("1", "impossible", None)
        sp = stats.get_single_player_stats()
        assert "easy" in sp
        assert "hard" in sp
        assert "impossible" in sp
        assert stats.get_total_games() == 3
        os.unlink(path)


# ===========================
# --- GameConfig Tests ---
# ===========================

class TestGameConfig:
    def test_default_delays_are_positive(self):
        assert GameConfig.AI_THINK_DELAY_SINGLE > 0
        assert GameConfig.AI_THINK_DELAY_AI_VS_AI > 0

    def test_timed_mode_options(self):
        assert len(GameConfig.TIMED_MODE_OPTIONS) >= 2
        for opt in GameConfig.TIMED_MODE_OPTIONS:
            assert opt > 0

    def test_tournament_options(self):
        for opt in GameConfig.TOURNAMENT_OPTIONS:
            assert opt % 2 == 1  # must be odd for best-of-N

    def test_adjustment_thresholds(self):
        assert 0 < GameConfig.ADJUST_DOWNGRADE_WIN_RATE < GameConfig.ADJUST_UPGRADE_WIN_RATE <= 1.0
        assert GameConfig.ADJUST_MIN_GAMES >= 1


# ===========================
# --- Tournament Tests ---
# ===========================

class TestTournament:
    def test_create_best_of_3(self):
        t = Tournament(3)
        assert t.best_of == 3
        assert t.wins_needed == 2
        assert t.round_number == 0

    def test_create_best_of_5(self):
        t = Tournament(5)
        assert t.wins_needed == 3

    def test_invalid_series_length(self):
        import pytest
        with pytest.raises(ValueError):
            Tournament(4)

    def test_record_round_not_over(self):
        t = Tournament(3)
        over = t.record_round("X")
        assert over is False
        assert t.wins["X"] == 1
        assert t.round_number == 1

    def test_series_ends_on_clinch(self):
        t = Tournament(3)
        t.record_round("X")
        over = t.record_round("X")
        assert over is True
        assert t.get_series_winner() == "X"

    def test_ties_dont_clinch(self):
        t = Tournament(3)
        t.record_round(None)
        t.record_round(None)
        assert t.is_over() is False
        assert t.get_series_winner() is None

    def test_full_series_with_ties(self):
        t = Tournament(3)
        t.record_round("X")
        t.record_round(None)
        t.record_round("O")
        assert t.is_over() is False
        t.record_round("O")
        assert t.is_over() is True
        assert t.get_series_winner() == "O"

    def test_results_tracked(self):
        t = Tournament(5)
        t.record_round("X")
        t.record_round("O")
        t.record_round(None)
        assert t.results == ["X", "O", None]

    def test_status_line_starting(self):
        t = Tournament(3)
        status = t.get_status_line()
        assert "Round 1/3" in status

    def test_status_line_leading(self):
        t = Tournament(5)
        t.record_round("X")
        status = t.get_status_line()
        assert "X leads" in status


# ===========================
# --- Difficulty Suggestion Tests ---
# ===========================

class TestDifficultySuggestion:
    def _make_stats(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.unlink(path)
        return GameStats(filepath=path), path

    def test_no_suggestion_too_few_games(self):
        stats, path = self._make_stats()
        for _ in range(4):  # under threshold of 5
            stats.record_game("1", "easy", "X")
        assert stats.get_difficulty_suggestion("easy") is None
        os.unlink(path)

    def test_suggest_up_when_dominating(self):
        stats, path = self._make_stats()
        for _ in range(5):
            stats.record_game("1", "easy", "X")
        assert stats.get_difficulty_suggestion("easy") == "up"
        os.unlink(path)

    def test_suggest_down_when_struggling(self):
        stats, path = self._make_stats()
        for _ in range(5):
            stats.record_game("1", "hard", "O")  # loss
        assert stats.get_difficulty_suggestion("hard") == "down"
        os.unlink(path)

    def test_no_suggestion_when_balanced(self):
        stats, path = self._make_stats()
        for _ in range(3):
            stats.record_game("1", "medium", "X")
        for _ in range(3):
            stats.record_game("1", "medium", "O")
        assert stats.get_difficulty_suggestion("medium") is None
        os.unlink(path)

    def test_no_up_at_max_difficulty(self):
        stats, path = self._make_stats()
        for _ in range(5):
            stats.record_game("1", "impossible", "X")
        assert stats.get_difficulty_suggestion("impossible") is None
        os.unlink(path)

    def test_no_down_at_min_difficulty(self):
        stats, path = self._make_stats()
        for _ in range(5):
            stats.record_game("1", "easy", "O")
        assert stats.get_difficulty_suggestion("easy") is None
        os.unlink(path)

    def test_no_suggestion_for_unplayed_difficulty(self):
        stats, path = self._make_stats()
        assert stats.get_difficulty_suggestion("hard") is None
        if os.path.exists(path):
            os.unlink(path)
