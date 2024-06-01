import numpy as np

# Constants
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
WIN_LENGTH = 5
INFINITY = float('inf')


class CaroGame:
    def __init__(self, size=15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = PLAYER_X

    def print_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == EMPTY

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            return True
        else:
            return False

    def is_winner(self, player):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player:
                    # Check horizontally
                    if j <= self.size - WIN_LENGTH:
                        if all(self.board[i][j+k] == player for k in range(WIN_LENGTH)):
                            return True
                    # Check vertically
                    if i <= self.size - WIN_LENGTH:
                        if all(self.board[i+k][j] == player for k in range(WIN_LENGTH)):
                            return True
                    # Check diagonally (down-right)
                    if i <= self.size - WIN_LENGTH and j <= self.size - WIN_LENGTH:
                        if all(self.board[i+k][j+k] == player for k in range(WIN_LENGTH)):
                            return True
                    # Check diagonally (down-left)
                    if i <= self.size - WIN_LENGTH and j >= WIN_LENGTH - 1:
                        if all(self.board[i+k][j-k] == player for k in range(WIN_LENGTH)):
                            return True
        return False

    def is_full(self):
        return np.all(self.board != EMPTY)

    def is_game_over(self):
        return self.is_winner(PLAYER_X) or self.is_winner(PLAYER_O) or self.is_full()


def minimax(game, depth, maximizingPlayer, alpha, beta):
    if depth == 0 or game.is_game_over():
        return evaluate(game)

    if maximizingPlayer:
        maxEval = -INFINITY
        for i in range(game.size):
            for j in range(game.size):
                if game.board[i][j] == EMPTY:
                    game.board[i][j] = PLAYER_X
                    eval = minimax(game, depth - 1, False, alpha, beta)
                    game.board[i][j] = EMPTY
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return maxEval
    else:
        minEval = INFINITY
        for i in range(game.size):
            for j in range(game.size):
                if game.board[i][j] == EMPTY:
                    game.board[i][j] = PLAYER_O
                    eval = minimax(game, depth - 1, True, alpha, beta)
                    game.board[i][j] = EMPTY
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return minEval


def evaluate(game):
    if game.is_winner(PLAYER_X):
        return 100
    elif game.is_winner(PLAYER_O):
        return -100
    else:
        return 0


def get_best_move(game):
    best_move = None
    best_eval = -INFINITY
    for i in range(game.size):
        for j in range(game.size):
            if game.board[i][j] == EMPTY:
                game.board[i][j] = PLAYER_X
                eval = minimax(game, 3, False, -INFINITY, INFINITY)  # Adjust depth as needed
                game.board[i][j] = EMPTY
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move


def main():
    game = CaroGame()

    while not game.is_game_over():
        game.print_board()

        if game.current_player == PLAYER_X:
            print("Player X's turn")
            row, col = map(int, input("Enter your move (row col): ").split())
            if game.make_move(row, col):
                if game.is_winner(PLAYER_X):
                    print("Player X wins!")
                    break
                game.current_player = PLAYER_O
            else:
                print("Invalid move, try again.")
        else:
            print("Player O's turn (AI)")
            row, col = get_best_move(game)
            game.make_move(row, col)
            if game.is_winner(PLAYER_O):
                print("Player O wins!")
                break
            game.current_player = PLAYER_X

    game.print_board()
    print("Game over")


if __name__ == "__main__":
    main()
