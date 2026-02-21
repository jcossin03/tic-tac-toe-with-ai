# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board
# Weekend 2: Taking Turns
# Weekend 3: Winning & Ending

# The board is a list of lists (a 2D list).
# Think of it like a grid of boxes - 3 rows, each with 3 spaces.
# Each space starts with a number so players know where to play.

board = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]


def display_board(board):
    """Show the tic-tac-toe board in a nice format."""
    print()
    for i, row in enumerate(board):
        print("  " + row[0] + " | " + row[1] + " | " + row[2])
        if i < 2:
            print("  " + "-" * 9)
    print()


def get_move(player):
    """Ask the player to pick a spot and make sure it's valid.

    This function uses a while loop - it keeps asking until
    the player gives a good answer (a number 1-9 that isn't taken).
    """
    while True:
        move = input("Player " + player + ", pick a spot (1-9): ")

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


def place_move(row, col, player):
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


# --- Game Start! ---
print("Welcome to Tic-Tac-Toe!")
print("Player X goes first, then Player O takes turns.")
display_board(board)

# current_player keeps track of whose turn it is
# We switch between "X" and "O" each turn
current_player = "X"

# The game loop - keeps going for up to 9 turns (the whole board)
for turn in range(9):
    # Ask the current player for their move
    row, col = get_move(current_player)

    # Place their mark on the board
    place_move(row, col, current_player)

    # Show the updated board
    display_board(board)

    # Check if the current player just won!
    winner = check_winner(board)
    if winner:
        print("Player " + winner + " wins! Congratulations!")
        break

    # Check if the board is full (tie game)
    if check_tie(board):
        print("It's a tie! Great game, everyone!")
        break

    # Switch to the other player
    # if/else: if it's X's turn, switch to O. Otherwise switch to X.
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
