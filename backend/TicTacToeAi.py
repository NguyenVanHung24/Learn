import copy
import random
from AI import *

def get_move(board, size,player):
    #Find all available positions on the board
    size = int(size)
    boardcoppy = copy.deepcopy(board)
    # Convert board to use 0 for empty spaces and 1 for 'x' marks
    for i in range(len(boardcoppy)):
        for j in range(len(boardcoppy[i])):
            if boardcoppy[i][j] == ' ':
                boardcoppy[i][j] = 0
            elif boardcoppy[i][j] == 'x':
                boardcoppy[i][j] = 1
            elif boardcoppy[i][j] == 'o':
                boardcoppy[i][j] = -1
    ai = AI(size,player)
    available_moves = ai.calcNextMove(boardcoppy, 3)
    # for i in range(size):
    #     for j in range(size):
    #         if board[i][j] == ' ':
    #             available_moves.append((i, j))

    # If there are no available moves, return None
    if not available_moves:
        return None
    # Choose a random available move
    return available_moves

    # size = int(size)
    # available_moves = []
    # for i in range(size):
    #     for j in range(size):
    #         if board[i][j] == ' ':
    #             available_moves.append((i, j))

    # # If there are no available moves, return None
    # if not available_moves:
    #     return None
    # # Choose a random available move
    # return available_moves[random.randint(0, len(available_moves) - 1)]