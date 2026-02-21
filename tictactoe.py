# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board
# Weekend 2: Taking Turns
# Weekend 3: Winning & Ending
# Weekend 4: Polish & Features
# Weekend 5-6: AI Player

import os
import sys
import random
import time

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


def colorize(text):
    """Add color to a board character based on what it is.

    - Numbers (available spots): dim gray so they're subtle
    - X marks: bold cyan so they pop
    - O marks: bold red so they're clearly different from X
    - Anything else: no color
    """
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


def display_board(board):
    """Show the tic-tac-toe board in a large, colorful format.

    Each cell is 3 rows tall and 5 characters wide so the board
    is easy to read. Colors make X, O, and numbers visually distinct.
    """
    print()
    print("  ╔═════╦═════╦═════╗")
    for i, row in enumerate(board):
        # Top padding row (empty space inside each cell)
        print("  ║     ║     ║     ║")
        # Middle row with the actual mark/number, centered
        c0 = colorize(row[0])
        c1 = colorize(row[1])
        c2 = colorize(row[2])
        print(f"  ║  {c0}  ║  {c1}  ║  {c2}  ║")
        # Bottom padding row
        print("  ║     ║     ║     ║")
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

    Returns "easy" or "hard".
    Easy = random moves. Hard = smart strategy (blocks and wins).
    """
    print()
    print("=== Difficulty ===")
    print(f"  {BOLD}{GREEN}1{RESET} - Easy   (computer picks randomly)")
    print(f"  {BOLD}{RED}2{RESET} - Hard   (computer tries to win and blocks you)")
    print()
    while True:
        choice = input("Choose difficulty (1 or 2): ").strip()
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "hard"
        print("Please enter 1 or 2.")


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

def reset_board():
    """Create a fresh board with numbers 1-9.

    We need this to start a new game without leftover X's and O's.
    Returns a brand new 2D list.
    """
    return [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]


def get_open_spots(board):
    """Find all the open spots on the board.

    Returns a list of (row, col) tuples for spots that aren't taken.
    This is used by the computer to know where it can play.

    A list comprehension is a shortcut for building a list.
    It's like saying "give me every (row, col) where the spot isn't X or O".
    """
    spots = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ["X", "O"]:
                spots.append((row, col))
    return spots


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
        # For example: spot 1 is row 0, col 0  |  spot 5 is row 1, col 1
        spot = int(move) - 1
        row = spot // 3
        col = spot % 3

        # Check if that spot is already taken (has an X or O)
        if board[row][col] in ["X", "O"]:
            print("That spot is already taken! Try again.")
            continue

        # If we get here, the move is good!
        return row, col


def place_move(board, row, col, player):
    """Put the player's mark (X or O) on the board."""
    board[row][col] = player


def check_winner(board):
    """Check if someone has won the game.

    Returns the winning player ("X" or "O") if there's a winner,
    or None if no one has won yet.

    There are 3 ways to win tic-tac-toe:
    1. Three in a row (horizontal)
    2. Three in a column (vertical)
    3. Three in a diagonal
    """

    # --- Check horizontal wins (rows) ---
    # Look at each row: if all 3 spots match, that player wins!
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]

    # --- Check vertical wins (columns) ---
    # This is trickier - we need to look DOWN each column.
    # board[0][col] is the top, board[1][col] is the middle,
    # board[2][col] is the bottom.
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # --- Check diagonal wins ---
    # Top-left to bottom-right: (0,0), (1,1), (2,2)
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # Top-right to bottom-left: (0,2), (1,1), (2,0)
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # No winner yet
    return None


def check_tie(board):
    """Check if the board is full (all spots taken).

    Returns True if every spot has an X or O (no numbers left).
    Returns False if there are still open spots.

    We loop through every row and every spot - if we find any
    spot that isn't X or O, the board isn't full yet.
    """
    for row in board:
        for spot in row:
            if spot not in ["X", "O"]:
                return False
    return True


# =========================
# --- AI Functions ---
# =========================

def get_computer_move_easy(board):
    """Computer picks a random open spot (Easy mode).

    Uses random.choice() to pick randomly from the list of open spots.
    This is the simplest AI - it doesn't think, just picks!
    """
    open_spots = get_open_spots(board)
    return random.choice(open_spots)


def find_winning_move(board, player):
    """Check if the given player can win on their next move.

    Try placing the player's mark in each open spot. If that
    creates a win, return that spot. Otherwise return None.

    This is "what if" thinking - we temporarily try a move,
    check if it wins, then undo it.
    """
    open_spots = get_open_spots(board)

    for row, col in open_spots:
        # Temporarily place the mark
        original = board[row][col]
        board[row][col] = player

        # Check if this move wins
        if check_winner(board) == player:
            # Undo the move and return this winning spot
            board[row][col] = original
            return (row, col)

        # Undo the move
        board[row][col] = original

    # No winning move found
    return None


def get_computer_move_hard(board, computer_mark, human_mark):
    """Computer uses strategy to pick the best move (Hard mode).

    Priority order (this is how the computer "thinks"):
    1. WIN:    If computer can win, take the winning move!
    2. BLOCK:  If human can win next turn, block them!
    3. CENTER: Take the center if it's open (strong position)
    4. CORNER: Take a corner if available (next best positions)
    5. RANDOM: Pick any open spot

    This is called priority-based decision making - check the most
    important things first, and fall back to less important options.
    """
    # 1. Can we WIN right now? Take it!
    winning_move = find_winning_move(board, computer_mark)
    if winning_move:
        return winning_move

    # 2. Can the HUMAN win next turn? Block them!
    blocking_move = find_winning_move(board, human_mark)
    if blocking_move:
        return blocking_move

    # 3. Take the CENTER if it's open (position 5 = row 1, col 1)
    if board[1][1] not in ["X", "O"]:
        return (1, 1)

    # 4. Take a CORNER if available
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    open_corners = [(r, c) for r, c in corners if board[r][c] not in ["X", "O"]]
    if open_corners:
        return random.choice(open_corners)

    # 5. Take any open spot (RANDOM fallback)
    return get_computer_move_easy(board)


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


def play_game(board, names, scores, game_mode, difficulty):
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
            # Computer's turn - pick a move based on difficulty
            print(f"{MAGENTA}{names['O']} is thinking...{RESET}")
            time.sleep(0.8)  # Short pause so it feels like the computer is thinking

            if difficulty == "easy":
                row, col = get_computer_move_easy(board)
            else:
                row, col = get_computer_move_hard(board, "O", "X")
        else:
            # Human's turn - ask for input
            row, col = get_move(board, current_player, names[current_player])

        # Place their mark on the board
        place_move(board, row, col, current_player)

        # Clear screen and redraw everything
        clear_screen()
        print("=== Tic-Tac-Toe ===")
        if game_mode == "1":
            diff_label = f"{GREEN}Easy{RESET}" if difficulty == "easy" else f"{RED}Hard{RESET}"
            print(f"  Mode: vs Computer ({diff_label})")
        display_scoreboard(names, scores)
        display_board(board)

        # Show what the computer played
        if is_computer_turn:
            spot_number = row * 3 + col + 1
            print(f"{MAGENTA}{names['O']} played spot {spot_number}{RESET}")
            print()

        # Check if the current player just won!
        winner = check_winner(board)
        if winner:
            color = CYAN if winner == "X" else RED
            print(f"{GREEN}*** {BOLD}{color}{names[winner]}{RESET}{GREEN} ({BOLD}{color}{winner}{RESET}{GREEN}) wins! Congratulations! ***{RESET}")
            scores[winner] += 1
            return

        # Check if the board is full (tie game)
        if check_tie(board):
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

clear_screen()
display_banner(["Welcome to", "TIC-TAC-TOE!"])
print()

# Choose game mode: 1 player or 2 players
game_mode = get_game_mode()

# If single player, choose difficulty
difficulty = None
if game_mode == "1":
    difficulty = get_difficulty()

# Get player names (computer name is automatic in 1-player mode)
names = get_player_names(game_mode)

# Scores are stored in a dictionary - easy to look up by key
scores = {"X": 0, "O": 0, "tie": 0}

# Outer game loop - keeps playing until they want to stop
playing = True
while playing:
    # Reset the board for a fresh game
    board = reset_board()

    # Show the starting state
    clear_screen()
    print("=== Tic-Tac-Toe ===")
    if game_mode == "1":
        diff_label = f"{GREEN}Easy{RESET}" if difficulty == "easy" else f"{RED}Hard{RESET}"
        print(f"  Mode: vs Computer ({diff_label})")
    display_scoreboard(names, scores)
    display_board(board)
    color_x = BOLD + CYAN + names['X'] + RESET
    print(f"{color_x} (X) goes first!")
    print()

    # Play one complete game
    play_game(board, names, scores, game_mode, difficulty)

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
