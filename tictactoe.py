# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board
# Weekend 2: Taking Turns

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

    # Switch to the other player
    # if/else: if it's X's turn, switch to O. Otherwise switch to X.
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

print("The board is full! Game over!")
