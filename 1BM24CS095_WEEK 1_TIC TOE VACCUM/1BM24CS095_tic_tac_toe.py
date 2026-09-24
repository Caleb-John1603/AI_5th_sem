import random
print("E CALEB JOHN 1BM24CS095")

# Function to print the game board
def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(board[i][j], end=" | ")
        print("\n-------------")

# Function to check if any player has won
def check_win(board, player):
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False

# Function to make a move for the computer
def make_computer_move(board):
    # Check if the computer can win in the next move
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if check_win(board, "O"):
                    return

                # Undo the move
                board[i][j] = " "

    # Check if the player can win in the next move
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                if check_win(board, "X"):
                    board[i][j] = "O"
                    return

                # Undo the move
                board[i][j] = " "

    # Choose a random move
    while True:
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        if board[i][j] == " ":
            board[i][j] = "O"
            return

# Function to play the game
def play_game():
    # Initialize the game board
    board = [[" " for _ in range(3)] for _ in range(3)]

    # Variable to keep track of the current player
    current_player = "X"

    # Main game loop
    while True:
        # Print the game board
        print_board(board)

        # Check if the current player is the user or the computer
        if current_player == "X":
            # Get the user's move
            while True:
                row = int(input("Enter the row (0-2): "))
                col = int(input("Enter the column (0-2): "))
                if board[row][col] == " ":
                    board[row][col] = "X"
                    break
                else:
                    print("Invalid move. Try again.")
        else:
            # Make the computer's move
            make_computer_move(board)

        # Check if the current player has won
        if check_win(board, current_player):
            print_board(board)
            print(f"{current_player} wins!")
            break

        # Check if the game is a tie
        if all(board[i][j] != " " for i in range(3) for j in range(3)):
            print_board(board)
            print("It's a tie!")
            break

        # Switch the current player
        current_player = "O" if current_player == "X" else "X"

# Start the game
play_game()
