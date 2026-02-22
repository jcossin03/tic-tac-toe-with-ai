# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board
# Weekend 2: Taking Turns
# Weekend 3: Winning & Ending
# Weekend 4: Polish & Features
# Weekend 5-6: AI Player
# Weekend 7: Refactor, new AI modes, move explanations

import os
import sys
import time

from game_logic import Board, AI

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

    print()
    print("  ╔═════╦═════╦═════╗")
    for i in range(3):
        # Top padding row (empty space inside each cell)
        top = "  ║"
        for j in range(3):
            if (i, j) in highlight_set:
                top += BG_GREEN + "     " + RESET
            else:
                top += "     "
            top += "║"
        print(top)

        # Middle row with the actual mark/number, centered
        mid = "  ║"
        for j in range(3):
            cell = board.get_cell(i, j)
            is_hl = (i, j) in highlight_set
            if is_hl:
                mid += BG_GREEN + " " + RESET + colorize(cell, highlight=True) + BG_GREEN + " " + RESET
            else:
                mid += "  " + colorize(cell) + "  "
            mid += "║"
        print(mid)

        # Bottom padding row
        bot = "  ║"
        for j in range(3):
            if (i, j) in highlight_set:
                bot += BG_GREEN + "     " + RESET
            else:
                bot += "     "
            bot += "║"
        print(bot)

        if i < 2:
            print("  ╠═════╬═════╬═════╣")
    print("  ╚═════╩═════╩═════╝")
    print()


def display_scoreboard(names, scores):
    """Show the current score between the two players.

    Uses f-strings - a way to put variables inside a string
    by writing f"text {variable} more text".

    The box width adjusts dynamically based on the content length
    so the top and bottom borders always match.
    """
    # Build the content line first so we can measure its length
    x_name = BOLD + CYAN + names['X'] + RESET
    o_name = BOLD + RED + names['O'] + RESET
    # Plain version (no color codes) to measure actual visible width
    plain = f" {names['X']}: {scores['X']}  vs  {names['O']}: {scores['O']}  Ties: {scores['tie']} "
    width = len(plain)
    # Colored version for display
    colored = f" {x_name}: {scores['X']}  vs  {o_name}: {scores['O']}  Ties: {scores['tie']} "
    # Build the box with matching borders
    print("  ┌" + "─" * width + "┐")
    print("  │" + colored + "│")
    print("  └" + "─" * width + "┘")


def display_banner(lines):
    """Display text inside a neat box banner.

    Takes a list of strings and wraps them in a box.
    Automatically sizes the box to fit the longest line.
    No emojis in the box to avoid alignment issues.
    """
    # Find the longest line to set the box width
    width = max(len(line) for line in lines) + 4  # +4 for padding
    print("  ╔" + "═" * width + "╗")
    for line in lines:
        # Center each line within the box
        padded = line.center(width)
        print("  ║" + padded + "║")
    print("  ╚" + "═" * width + "╝")


# =========================
# --- Menu Functions ---
# =========================

def get_game_mode():
    """Ask the player to choose 1-player or 2-player mode.

    Returns "1" for single player (vs computer) or "2" for two players.
    Uses a while loop to keep asking until we get a valid answer.
    """
    print("=== Game Mode ===")
    print(f"  {BOLD}1{RESET} - Single Player (vs Computer)")
    print(f"  {BOLD}2{RESET} - Two Players")
    print()
    while True:
        choice = input("Choose mode (1 or 2): ").strip()
        if choice in ["1", "2"]:
            return choice
        print("Please enter 1 or 2.")


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


def get_player_names(game_mode):
    """Ask players for their names based on game mode.

    In 1-player mode, only ask for the human's name.
    The computer gets a fun name automatically.
    In 2-player mode, ask both players for names.

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


def play_game(board, names, scores, game_mode, difficulty, ai=None):
    """Play one complete game of tic-tac-toe.

    This function contains the turn-by-turn game loop.
    It updates the scores dictionary when the game ends.
    In 1-player mode, the computer automatically takes its turn.
    """
    current_player = "X"

    # The game loop - keeps going for up to 9 turns (the whole board)
    for turn in range(9):

        # Decide if this turn is a human or computer
        is_computer_turn = (game_mode == "1" and current_player == "O")

        if is_computer_turn:
            # Computer's turn - pick a move using the AI object
            print(f"{MAGENTA}{names['O']} is thinking...{RESET}")
            time.sleep(0.8)  # Short pause so it feels like the computer is thinking

            row, col = ai.get_move(board)
        else:
            # Human's turn - ask for input
            row, col = get_move(board, current_player, names[current_player])

        # Place their mark on the board
        board.place_move(row, col, current_player)

        # Clear screen and redraw everything
        clear_screen()
        print("=== Tic-Tac-Toe ===")
        if game_mode == "1":
            diff_label = get_difficulty_label(difficulty)
            print(f"  Mode: vs Computer ({diff_label})")
        display_scoreboard(names, scores)

        # Check if the current player just won!
        winner = board.check_winner()
        winning_line = board.get_winning_line() if winner else None

        display_board(board, winning_line=winning_line)

        # Show what the computer played (and why)
        if is_computer_turn:
            spot_number = Board.coords_to_spot(row, col)
            print(f"{MAGENTA}{names['O']} played spot {spot_number}{RESET}")
            if ai.last_explanation:
                print(f"  {DIM}({ai.last_explanation}){RESET}")
            print()

        if winner:
            color = CYAN if winner == "X" else RED
            print(f"{GREEN}*** {BOLD}{color}{names[winner]}{RESET}{GREEN} ({BOLD}{color}{winner}{RESET}{GREEN}) wins! Congratulations! ***{RESET}")
            scores[winner] += 1
            return

        # Check if the board is full (tie game)
        if board.is_full():
            print(f"{YELLOW}It's a tie! Great game, everyone!{RESET}")
            scores["tie"] += 1
            return

        # Switch to the other player
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


# ======================
# --- Program Start! ---
# ======================

if __name__ == "__main__":
    clear_screen()
    display_banner(["Welcome to", "TIC-TAC-TOE!"])
    print()

    # Choose game mode: 1 player or 2 players
    game_mode = get_game_mode()

    # If single player, choose difficulty
    difficulty = None
    ai = None
    if game_mode == "1":
        difficulty = get_difficulty()
        ai = AI(difficulty, mark="O", opponent_mark="X")

    # Get player names (computer name is automatic in 1-player mode)
    names = get_player_names(game_mode)

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
        if game_mode == "1":
            diff_label = get_difficulty_label(difficulty)
            print(f"  Mode: vs Computer ({diff_label})")
        display_scoreboard(names, scores)
        display_board(board)
        color_x = BOLD + CYAN + names['X'] + RESET
        print(f"{color_x} (X) goes first!")
        print()

        # Play one complete game
        play_game(board, names, scores, game_mode, difficulty, ai)

        # Show final score and ask to play again
        print()
        display_scoreboard(names, scores)
        print()
        playing = play_again()

    # Goodbye message
    clear_screen()
    display_banner(["Thanks for playing!"])
    print()
    print("=== Final Scores ===")
    display_scoreboard(names, scores)
    print()
    print("See you next time!")
