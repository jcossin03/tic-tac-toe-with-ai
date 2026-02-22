# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board
# Weekend 2: Taking Turns
# Weekend 3: Winning & Ending
# Weekend 4: Polish & Features
# Weekend 5-6: AI Player
# Weekend 7: Refactor, new AI modes, move explanations

import os
import random
import sys
import threading
import time

from game_logic import Board, AI, GameStats, GameConfig, Tournament

# Make sure the terminal can display our fancy box characters (╔, ═, etc.)
# This tells Python to use UTF-8 encoding for output.
sys.stdout.reconfigure(encoding="utf-8")

# On Windows, enable ANSI color support in the terminal.
# Without this, color codes show up as garbled text instead of colors.
if os.name == "nt":
    os.system("")


# =========================
# --- Color Helpers ---
# =========================

# ANSI escape codes for colors.
# These are special character sequences that tell the terminal
# to change the text color. Think of them like invisible paint instructions.
# "\033[" starts the code, the number picks the color, and "m" ends it.

RESET = "\033[0m"       # Turn off all colors (back to normal)
DIM = "\033[2m"          # Dim/faded text (for available numbers)
BOLD = "\033[1m"         # Bold text
CYAN = "\033[96m"        # Bright cyan (for X)
RED = "\033[91m"         # Bright red (for O)
YELLOW = "\033[93m"      # Bright yellow (for banners)
GREEN = "\033[92m"       # Bright green (for win messages)
MAGENTA = "\033[95m"     # Bright magenta (for computer player)
BG_GREEN = "\033[42m"    # Green background (for winning line highlight)
WHITE = "\033[97m"       # Bright white (for winning marks on green bg)


def colorize(text, highlight=False):
    """Add color to a board character based on what it is.

    - Numbers (available spots): dim gray so they're subtle
    - X marks: bold cyan so they pop
    - O marks: bold red so they're clearly different from X
    - If highlight=True: green background to show the winning line
    """
    if highlight and text in ["X", "O"]:
        return BG_GREEN + BOLD + WHITE + " " + text + " " + RESET
    if text == "X":
        return BOLD + CYAN + text + RESET
    elif text == "O":
        return BOLD + RED + text + RESET
    elif text in "123456789":
        return DIM + text + RESET
    return text


# =========================
# --- Display Functions ---
# =========================

def clear_screen():
    """Clear the terminal screen so the board doesn't scroll.

    os.system() runs a command in the terminal.
    'cls' is the Windows command to clear the screen.
    'clear' is the Mac/Linux command.
    os.name tells us which operating system we're on:
      'nt' means Windows, anything else means Mac/Linux.
    """
    os.system("cls" if os.name == "nt" else "clear")


def display_board(board, winning_line=None):
    """Show the tic-tac-toe board in a large, colorful format.

    Each cell is 3 rows tall and 5 characters wide so the board
    is easy to read. Colors make X, O, and numbers visually distinct.
    If winning_line is provided, those cells get a green background.
    """
    highlight_set = set(winning_line) if winning_line else set()

    cfg = GameConfig
    pad = " " * cfg.CELL_WIDTH

    print()
    print("  " + cfg.BOX_TOP)
    for i in range(3):
        # Top padding row (empty space inside each cell)
        top = "  " + cfg.BOX_V
        for j in range(3):
            if (i, j) in highlight_set:
                top += BG_GREEN + pad + RESET
            else:
                top += pad
            top += cfg.BOX_V
        print(top)

        # Middle row with the actual mark/number, centered
        mid = "  " + cfg.BOX_V
        for j in range(3):
            cell = board.get_cell(i, j)
            is_hl = (i, j) in highlight_set
            if is_hl:
                mid += BG_GREEN + " " + RESET + colorize(cell, highlight=True) + BG_GREEN + " " + RESET
            else:
                mid += "  " + colorize(cell) + "  "
            mid += cfg.BOX_V
        print(mid)

        # Bottom padding row
        bot = "  " + cfg.BOX_V
        for j in range(3):
            if (i, j) in highlight_set:
                bot += BG_GREEN + pad + RESET
            else:
                bot += pad
            bot += cfg.BOX_V
        print(bot)

        if i < 2:
            print("  " + cfg.BOX_MID)
    print("  " + cfg.BOX_BOT)
    print()


def display_scoreboard(names, scores):
    """Show the current score between the two players.

    Uses f-strings - a way to put variables inside a string
    by writing f"text {variable} more text".

    The box width adjusts dynamically based on the content length
    so the top and bottom borders always match.
    """
    cfg = GameConfig
    # Build the content line first so we can measure its length
    x_name = BOLD + CYAN + names['X'] + RESET
    o_name = BOLD + RED + names['O'] + RESET
    # Plain version (no color codes) to measure actual visible width
    plain = f" {names['X']}: {scores['X']}  vs  {names['O']}: {scores['O']}  Ties: {scores['tie']} "
    width = len(plain)
    # Colored version for display
    colored = f" {x_name}: {scores['X']}  vs  {o_name}: {scores['O']}  Ties: {scores['tie']} "
    # Build the box with matching borders
    print("  " + cfg.SCORE_TOP_LEFT + cfg.SCORE_H * width + cfg.SCORE_TOP_RIGHT)
    print("  │" + colored + "│")
    print("  " + cfg.SCORE_BOT_LEFT + cfg.SCORE_H * width + cfg.SCORE_BOT_RIGHT)


def display_banner(lines):
    """Display text inside a neat box banner.

    Takes a list of strings and wraps them in a box.
    Automatically sizes the box to fit the longest line.
    No emojis in the box to avoid alignment issues.
    """
    cfg = GameConfig
    # Find the longest line to set the box width
    width = max(len(line) for line in lines) + 4  # +4 for padding
    print("  " + cfg.BANNER_TOP_LEFT + cfg.BANNER_H * width + cfg.BANNER_TOP_RIGHT)
    for line in lines:
        # Center each line within the box
        padded = line.center(width)
        print("  " + cfg.BANNER_V + padded + cfg.BANNER_V)
    print("  " + cfg.BANNER_BOT_LEFT + cfg.BANNER_H * width + cfg.BANNER_BOT_RIGHT)


# =========================
# --- Menu Functions ---
# =========================

def get_game_mode():
    """Ask the player to choose a game mode.

    Returns "1" for single player, "2" for two players, "3" for AI vs AI,
    or "4" for tournament mode.
    Uses a while loop to keep asking until we get a valid answer.
    """
    print("=== Game Mode ===")
    print(f"  {BOLD}1{RESET} - Single Player (vs Computer)")
    print(f"  {BOLD}2{RESET} - Two Players")
    print(f"  {BOLD}3{RESET} - AI vs AI (Watch Mode)")
    print(f"  {BOLD}4{RESET} - Tournament (Best-of-N Series)")
    print()
    while True:
        choice = input("Choose mode (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("Please enter 1, 2, 3, or 4.")


def get_difficulty():
    """Ask the player to choose a difficulty level for the computer.

    Returns "easy", "medium", "hard", or "impossible".
    """
    print()
    print("=== Difficulty ===")
    print(f"  {BOLD}{GREEN}1{RESET} - Easy       (computer picks randomly)")
    print(f"  {BOLD}{YELLOW}2{RESET} - Medium     (mix of random and strategic)")
    print(f"  {BOLD}{RED}3{RESET} - Hard       (computer tries to win and blocks you)")
    print(f"  {BOLD}{MAGENTA}4{RESET} - Impossible (computer never loses - minimax AI)")
    print()
    while True:
        choice = input("Choose difficulty (1-4): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "medium"
        elif choice == "3":
            return "hard"
        elif choice == "4":
            return "impossible"
        print("Please enter 1, 2, 3, or 4.")


def get_difficulty_label(difficulty):
    """Return a colored label for the current difficulty."""
    labels = {
        "easy": f"{GREEN}Easy{RESET}",
        "medium": f"{YELLOW}Medium{RESET}",
        "hard": f"{RED}Hard{RESET}",
        "impossible": f"{MAGENTA}Impossible{RESET}",
    }
    return labels.get(difficulty, difficulty)


def get_tournament_length():
    """Ask the player to choose a tournament series length.

    Returns 3, 5, or 7.
    """
    print()
    print("=== Tournament Length ===")
    for opt in GameConfig.TOURNAMENT_OPTIONS:
        print(f"  {BOLD}{opt}{RESET} - Best of {opt}")
    print()
    valid = [str(o) for o in GameConfig.TOURNAMENT_OPTIONS]
    while True:
        choice = input(f"Choose series length ({', '.join(valid)}): ").strip()
        if choice in valid:
            return int(choice)
        print(f"Please enter {', '.join(valid)}.")


def get_tournament_type():
    """Ask what type of tournament game (vs Computer or vs Player).

    Returns "1" for single player or "2" for two player.
    """
    print()
    print("=== Tournament Type ===")
    print(f"  {BOLD}1{RESET} - vs Computer")
    print(f"  {BOLD}2{RESET} - vs Player")
    print()
    while True:
        choice = input("Choose (1 or 2): ").strip()
        if choice in ["1", "2"]:
            return choice
        print("Please enter 1 or 2.")


def display_tournament_status(tournament, names):
    """Show the tournament bracket/progress between rounds."""
    t = tournament
    print(f"  {YELLOW}=== Tournament: Best of {t.best_of} ==={RESET}")
    x_name = BOLD + CYAN + names['X'] + RESET
    o_name = BOLD + RED + names['O'] + RESET
    print(f"  {x_name}: {t.wins['X']} wins  |  {o_name}: {t.wins['O']} wins  |  Ties: {t.wins['tie']}")
    if t.results:
        rounds_str = "  Rounds: "
        for i, result in enumerate(t.results, 1):
            if result == "X":
                rounds_str += f"{CYAN}X{RESET} "
            elif result == "O":
                rounds_str += f"{RED}O{RESET} "
            else:
                rounds_str += f"{DIM}T{RESET} "
        print(rounds_str)
    winner = t.get_series_winner()
    if winner:
        color = CYAN if winner == "X" else RED
        print(f"  {GREEN}*** {BOLD}{color}{names[winner]}{RESET}{GREEN} wins the series! ***{RESET}")
    elif not t.is_over():
        print(f"  {DIM}{t.get_status_line()}{RESET}")
    print()


def get_timed_mode():
    """Ask if the player wants timed moves.

    Returns the time limit in seconds, or None for untimed.
    """
    print()
    print("=== Timed Mode ===")
    print(f"  {BOLD}0{RESET} - No time limit")
    for secs in GameConfig.TIMED_MODE_OPTIONS:
        print(f"  {BOLD}{secs}{RESET} - {secs} seconds per move")
    print()
    valid = ["0"] + [str(s) for s in GameConfig.TIMED_MODE_OPTIONS]
    while True:
        choice = input(f"Choose time limit ({', '.join(valid)}): ").strip()
        if choice in valid:
            val = int(choice)
            return val if val > 0 else None
        print(f"Please enter {', '.join(valid)}.")


def get_timed_move(board, player, player_name, time_limit):
    """Get a move with a countdown timer. Returns (row, col).

    If the player doesn't move in time, a random valid move is made for them.
    Uses a background thread for input so the main thread can count down.
    """
    color = CYAN if player == "X" else RED
    colored_mark = BOLD + color + player + RESET

    result = {"move": None}

    def read_input():
        while result["move"] is None:
            try:
                move = input(f"{player_name} ({colored_mark}), pick a spot (1-9) [{time_limit}s]: ")
                if move not in "123456789" or len(move) != 1:
                    print("Oops! Please enter a number from 1 to 9.")
                    continue
                row, col = Board.spot_to_coords(move)
                if not board.is_valid_move(row, col):
                    print("That spot is already taken! Try again.")
                    continue
                result["move"] = (row, col)
                return
            except EOFError:
                return

    input_thread = threading.Thread(target=read_input, daemon=True)
    input_thread.start()
    input_thread.join(timeout=time_limit)

    if result["move"] is not None:
        return result["move"]

    # Time expired — pick a random valid move
    spots = board.get_open_spots()
    move = random.choice(spots)
    print(f"\n{YELLOW}Time's up! A random move was made.{RESET}")
    return move


def get_first_player():
    """Ask who should go first.

    Returns "X" or "O".
    """
    print()
    print("=== Who Goes First? ===")
    print(f"  {BOLD}1{RESET} - {BOLD}{CYAN}X{RESET} goes first")
    print(f"  {BOLD}2{RESET} - {BOLD}{RED}O{RESET} goes first")
    print()
    while True:
        choice = input("Choose (1 or 2): ").strip()
        if choice == "1":
            return "X"
        elif choice == "2":
            return "O"
        print("Please enter 1 or 2.")


def get_player_names(game_mode):
    """Ask players for their names based on game mode.

    In 1-player mode, only ask for the human's name.
    The computer gets a fun name automatically.
    In 2-player mode, ask both players for names.
    In AI vs AI mode, both are named by their difficulty.

    Returns a dictionary that maps 'X' and 'O' to player names.
    """
    print()
    print("=== Player Setup ===")

    if game_mode == "1":
        name_x = input(f"Enter your name ({BOLD}{CYAN}X{RESET}): ").strip()
        if not name_x:
            name_x = "Player X"
        name_o = "Computer"
        return {"X": name_x, "O": name_o}
    elif game_mode == "3":
        return {"X": "AI-X", "O": "AI-O"}
    else:
        name_x = input(f"Enter name for Player {BOLD}{CYAN}X{RESET}: ").strip()
        name_o = input(f"Enter name for Player {BOLD}{RED}O{RESET}: ").strip()
        if not name_x:
            name_x = "Player X"
        if not name_o:
            name_o = "Player O"
        return {"X": name_x, "O": name_o}


# =========================
# --- Game Logic ---
# =========================

def get_move(board, player, player_name):
    """Ask the player to pick a spot and make sure it's valid.

    This function uses a while loop - it keeps asking until
    the player gives a good answer (a number 1-9 that isn't taken).
    """
    # Color the player's mark in the prompt
    color = CYAN if player == "X" else RED
    colored_mark = BOLD + color + player + RESET

    while True:
        move = input(f"{player_name} ({colored_mark}), pick a spot (1-9): ")

        # Check if they typed a number
        if move not in "123456789" or len(move) != 1:
            print("Oops! Please enter a number from 1 to 9.")
            continue

        # Turn the number into a row and column on the board
        row, col = Board.spot_to_coords(move)

        # Check if that spot is already taken (has an X or O)
        if not board.is_valid_move(row, col):
            print("That spot is already taken! Try again.")
            continue

        # If we get here, the move is good!
        return row, col


# =========================
# --- Game Play ---
# =========================

def play_again():
    """Ask if the players want to play another game.

    Returns True if yes, False if no.
    .lower() converts their answer to lowercase so 'Y', 'y', 'YES' all work.
    """
    while True:
        answer = input("Play again? (y/n): ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def display_move_history(move_log, names):
    """Show a post-game summary of all moves in order."""
    if not move_log:
        return
    print("=== Move History ===")
    for i, (player, spot) in enumerate(move_log, 1):
        color = CYAN if player == "X" else RED
        mark = BOLD + color + player + RESET
        print(f"  {DIM}{i:2d}.{RESET} {names[player]} ({mark}) -> spot {spot}")
    print()


def play_game(board, names, scores, game_mode, difficulty, ai=None, ai_x=None, first_player="X", time_limit=None):
    """Play one complete game of tic-tac-toe.

    This function contains the turn-by-turn game loop.
    It updates the scores dictionary when the game ends.
    In 1-player mode, the computer automatically takes its turn.
    In AI vs AI mode, both players are controlled by AI.
    time_limit: seconds per move, or None for unlimited.
    Returns the winner ("X", "O") or None (tie).
    """
    current_player = first_player
    move_log = []

    # The game loop - keeps going for up to 9 turns (the whole board)
    for turn in range(9):

        # Decide if this turn is a human or computer
        is_computer_turn = False
        active_ai = None
        if game_mode == "3":
            # AI vs AI mode - both sides are computer
            is_computer_turn = True
            active_ai = ai_x if current_player == "X" else ai
        elif game_mode == "1" and current_player == "O":
            is_computer_turn = True
            active_ai = ai

        if is_computer_turn:
            # Computer's turn
            color = CYAN if current_player == "X" else RED
            print(f"{MAGENTA}{names[current_player]} is thinking...{RESET}")
            delay = GameConfig.AI_THINK_DELAY_SINGLE if game_mode == "1" else GameConfig.AI_THINK_DELAY_AI_VS_AI
            time.sleep(delay)

            row, col = active_ai.get_move(board)
        else:
            # Human's turn - ask for input (with optional timer)
            if time_limit:
                row, col = get_timed_move(board, current_player, names[current_player], time_limit)
            else:
                row, col = get_move(board, current_player, names[current_player])

        # Place their mark on the board
        board.place_move(row, col, current_player)
        spot_number = Board.coords_to_spot(row, col)
        move_log.append((current_player, spot_number))

        # Clear screen and redraw everything
        clear_screen()
        print("=== Tic-Tac-Toe ===")
        if game_mode == "1":
            diff_label = get_difficulty_label(difficulty)
            print(f"  Mode: vs Computer ({diff_label})")
        elif game_mode == "3":
            print(f"  Mode: AI vs AI (watching)")
        display_scoreboard(names, scores)

        # Check if the current player just won!
        winner = board.check_winner()
        winning_line = board.get_winning_line() if winner else None

        display_board(board, winning_line=winning_line)

        # Show what the computer played (and why)
        if is_computer_turn:
            color = CYAN if current_player == "X" else RED
            print(f"{MAGENTA}{names[current_player]} played spot {spot_number}{RESET}")
            if active_ai.last_explanation:
                print(f"  {DIM}({active_ai.last_explanation}){RESET}")
            print()

        if winner:
            color = CYAN if winner == "X" else RED
            print(f"{GREEN}*** {BOLD}{color}{names[winner]}{RESET}{GREEN} ({BOLD}{color}{winner}{RESET}{GREEN}) wins! Congratulations! ***{RESET}")
            scores[winner] += 1
            display_move_history(move_log, names)
            return winner

        # Check if the board is full (tie game)
        if board.is_full():
            print(f"{YELLOW}It's a tie! Great game, everyone!{RESET}")
            scores["tie"] += 1
            display_move_history(move_log, names)
            return None

        # Switch to the other player
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

        # In AI vs AI mode, pause briefly so the viewer can follow
        if game_mode == "3":
            input(f"{DIM}Press Enter to continue...{RESET}")


# ======================
# --- Program Start! ---
# ======================

def display_lifetime_stats(stats):
    """Show a summary of lifetime game statistics."""
    sp = stats.get_single_player_stats()
    tp = stats.get_two_player_stats()
    total = stats.get_total_games()
    if total == 0:
        return

    print("=== Lifetime Stats ===")
    if sp:
        print("  Single Player:")
        for diff in ["easy", "medium", "hard", "impossible"]:
            if diff in sp:
                e = sp[diff]
                games = e["wins"] + e["losses"] + e["ties"]
                label = get_difficulty_label(diff)
                print(f"    {label}: {e['wins']}W / {e['losses']}L / {e['ties']}T ({games} games)")
    tp_total = tp.get("wins_x", 0) + tp.get("wins_o", 0) + tp.get("ties", 0)
    if tp_total > 0:
        print(f"  Two Player: X {tp['wins_x']}W / O {tp['wins_o']}W / {tp['ties']}T ({tp_total} games)")
    print(f"  Total games played: {total}")
    print()


if __name__ == "__main__":
    clear_screen()
    display_banner(["Welcome to", "TIC-TAC-TOE!"])
    print()

    # Load persistent stats
    stats = GameStats()

    # Show lifetime stats if any games have been played
    display_lifetime_stats(stats)

    # Choose game mode: 1 player, 2 players, AI vs AI, or tournament
    game_mode = get_game_mode()

    # Tournament mode wraps around single-player or two-player
    tournament = None
    tournament_game_mode = None
    if game_mode == "4":
        best_of = get_tournament_length()
        tournament = Tournament(best_of)
        tournament_game_mode = get_tournament_type()
    else:
        tournament_game_mode = game_mode

    # If single player or AI vs AI, choose difficulty
    difficulty = None
    difficulty_x = None
    ai = None
    ai_x = None
    effective_mode = tournament_game_mode if game_mode == "4" else game_mode
    if effective_mode == "1":
        difficulty = get_difficulty()
        ai = AI(difficulty, mark="O", opponent_mark="X")
    elif effective_mode == "3":
        print()
        print(f"=== {BOLD}{CYAN}AI-X{RESET} Difficulty ===")
        difficulty_x = get_difficulty()
        ai_x = AI(difficulty_x, mark="X", opponent_mark="O")
        print()
        print(f"=== {BOLD}{RED}AI-O{RESET} Difficulty ===")
        difficulty = get_difficulty()
        ai = AI(difficulty, mark="O", opponent_mark="X")

    # Get player names (automatic in AI vs AI mode)
    names = get_player_names(effective_mode)
    if effective_mode == "3":
        names["X"] = f"AI-X ({difficulty_x.title()})"
        names["O"] = f"AI-O ({difficulty.title()})"

    # Choose who goes first
    first_player = "X"
    if effective_mode in ["1", "2"]:
        first_player = get_first_player()

    # Offer timed mode for human-involved games
    time_limit = None
    if effective_mode in ["1", "2"]:
        time_limit = get_timed_mode()

    # Scores are stored in a dictionary - easy to look up by key
    scores = {"X": 0, "O": 0, "tie": 0}

    # Outer game loop - keeps playing until they want to stop
    playing = True
    while playing:
        # Reset the board for a fresh game
        board = Board()

        # Show the starting state
        clear_screen()
        print("=== Tic-Tac-Toe ===")
        if effective_mode == "1":
            diff_label = get_difficulty_label(difficulty)
            print(f"  Mode: vs Computer ({diff_label})")
        elif effective_mode == "3":
            print(f"  Mode: AI vs AI")
        if time_limit:
            print(f"  Timer: {YELLOW}{time_limit}s per move{RESET}")
        if tournament and not tournament.is_over():
            display_tournament_status(tournament, names)
        display_scoreboard(names, scores)
        display_board(board)
        color = CYAN if first_player == "X" else RED
        starter_name = BOLD + color + names[first_player] + RESET
        print(f"{starter_name} ({first_player}) goes first!")
        print()

        # Play one complete game
        winner = play_game(board, names, scores, effective_mode, difficulty,
                           ai=ai, ai_x=ai_x, first_player=first_player,
                           time_limit=time_limit)

        # Record result in persistent stats
        if effective_mode != "3":
            stats.record_game(effective_mode, difficulty, winner)

        # Show final score
        print()
        display_scoreboard(names, scores)
        print()

        # Tournament mode: record round and check if series is over
        if tournament:
            series_over = tournament.record_round(winner)
            display_tournament_status(tournament, names)
            if series_over:
                playing = False
            else:
                input(f"{DIM}Press Enter for next round...{RESET}")
        else:
            playing = play_again()

    # Goodbye message
    clear_screen()
    display_banner(["Thanks for playing!"])
    print()
    print("=== Final Scores ===")
    display_scoreboard(names, scores)
    print()
    if tournament:
        display_tournament_status(tournament, names)
    display_lifetime_stats(stats)
    print("See you next time!")
