# Tic-Tac-Toe Game
# Weekend 1: Setup & Game Board

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


# Show the board!
print("Welcome to Tic-Tac-Toe!")
print("Here is your game board:")
display_board(board)
print("Each number shows where you can play.")
print("Pick a number 1-9 to place your mark!")
