# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board
# Weekend 2: Taking Turns
# Weekend 3: Winning & Ending
# Weekend 4: Polish & Features

import os
import sys

# Make sure the terminal can display our fancy box characters (╔, ═, etc.)
# This tells Python to use UTF-8 encoding for output.
sys.stdout.reconfigure(encoding="utf-8")


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
    """Show the tic-tac-toe board in a nice format with box borders."""
    print()
    print("  ╔═══╦═══╦═══╗")
    for i, row in enumerate(board):
        print("  ║ " + row[0] + " ║ " + row[1] + " ║ " + row[2] + " ║")
        if i < 2:
            print("  ╠═══╬═══╬═══╣")
    print("  ╚═══╩═══╩═══╝")
    print()


def display_scoreboard(names, scores):
    """Show the current score between the two players.

    Uses f-strings - a way to put variables inside a string
    by writing f"text {variable} more text".

    The box width adjusts dynamically based on the content length
    so the top and bottom borders always match.
    """
    # Build the content line first so we can measure its length
    content = f" {names['X']}: {scores['X']}  vs  {names['O']}: {scores['O']}  Ties: {scores['tie']} "
    # Calculate how wide the box needs to be
    width = len(content)
    # Build the box with matching borders
    print("  ┌" + "─" * width + "┐")
    print("  │" + content + "│")
    print("  └" + "─" * width + "┘")


def get_player_names():
    """Ask both players for their names at the start.

    Returns a dictionary that maps 'X' and 'O' to player names.
    A dictionary is like a labeled box - you look up a value by its label (key).
    """
    print("=== Player Setup ===")
    name_x = input("Enter name for Player X: ").strip()
    name_o = input("Enter name for Player O: ").strip()

    # If they left a name blank, use a default
    if not name_x:
        name_x = "Player X"
    if not name_o:
        name_o = "Player O"

    # Return a dictionary: the key is the mark, the value is the name
    return {"X": name_x, "O": name_o}


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


def get_move(board, player, player_name):
    """Ask the player to pick a spot and make sure it's valid.

    This function uses a while loop - it keeps asking until
    the player gives a good answer (a number 1-9 that isn't taken).
    """
    while True:
        move = input(f"{player_name} ({player}), pick a spot (1-9): ")

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


def play_game(board, names, scores):
    """Play one complete game of tic-tac-toe.

    This function contains the turn-by-turn game loop.
    It updates the scores dictionary when the game ends.
    """
    current_player = "X"

    # The game loop - keeps going for up to 9 turns (the whole board)
    for turn in range(9):
        # Ask the current player for their move
        row, col = get_move(board, current_player, names[current_player])

        # Place their mark on the board
        place_move(board, row, col, current_player)

        # Clear screen and redraw everything
        clear_screen()
        print("=== Tic-Tac-Toe ===")
        display_scoreboard(names, scores)
        display_board(board)

        # Check if the current player just won!
        winner = check_winner(board)
        if winner:
            print(f"🎉 {names[winner]} ({winner}) wins! Congratulations! 🎉")
            scores[winner] += 1
            return

        # Check if the board is full (tie game)
        if check_tie(board):
            print("It's a tie! Great game, everyone!")
            scores["tie"] += 1
            return

        # Switch to the other player
        # if/else: if it's X's turn, switch to O. Otherwise switch to X.
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


# ======================
# --- Program Start! ---
# ======================

clear_screen()
print("╔═══════════════════════╗")
print("║   Welcome to          ║")
print("║   TIC-TAC-TOE! 🎮    ║")
print("╚═══════════════════════╝")
print()

# Get player names
names = get_player_names()

# Scores are stored in a dictionary - easy to look up by key
# scores["X"] is Player X's wins, scores["O"] is Player O's wins
scores = {"X": 0, "O": 0, "tie": 0}

# Outer game loop - keeps playing until they want to stop
playing = True
while playing:
    # Reset the board for a fresh game
    board = reset_board()

    # Show the starting state
    clear_screen()
    print("=== Tic-Tac-Toe ===")
    display_scoreboard(names, scores)
    display_board(board)
    print(f"{names['X']} (X) goes first!")
    print()

    # Play one complete game
    play_game(board, names, scores)

    # Show final score and ask to play again
    print()
    display_scoreboard(names, scores)
    print()
    playing = play_again()

# Goodbye message
clear_screen()
print("╔═══════════════════════════╗")
print("║   Thanks for playing! 🎉  ║")
print("╚═══════════════════════════╝")
print()
print("=== Final Scores ===")
display_scoreboard(names, scores)
print()
print("See you next time!")
