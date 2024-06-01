import copy
import numpy as np

class AI:
    size=5
    winScore = 100000000
    # True là O 
    # False là X
    player = True 
    _instance = None

    def __new__(cls, size,player):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.size = size
            cls._instance.size = player
        return cls._instance

    def __init__(self,size,player) -> None:
        self.size=size
        self.player=player

    # Đánh giá điểm theo tình huống
    def getConsecutiveSetScore(self, count, blocks, currentTurn):
        winGuarantee = 1000000
        if blocks == 2 and count <= 5:
            return 0
        if count == 5:
            # Ăn 5 -> Cho điểm cao nhất
            return self.winScore
        if count == 4:
            # Đang 4 -> Tuỳ theo lược và bị chặn
            if currentTurn:
                return winGuarantee
            else:
                if blocks == 0:
                    return winGuarantee / 2
                else:
                    return winGuarantee / 4
        if count == 3:
            # Đang 3: Block = 0
            if blocks == 0:
                if currentTurn:
                    return 50000
                else:
                    return 50000 / 2
            else:
                # Block == 1 hoặc Blocks == 2
                if currentTurn:
                    return 10
                else:
                    return 5
        if count == 2:
            # Tương tự với 2
            if blocks == 0:
                if currentTurn:
                    return 7
                else:
                    return 5
            else:
                return 3
        if count == 1:
            return 1
        return self.winScore * 2

    def evaluateHorizontal(self,boardMatrix,ForX,playersTurn) :
        consecutive = 0
        blocks = 2
        score = 0
        board = np.array(boardMatrix)
        board = np.where(board != 0)
        minx = np.min(board[0])
        miny = np.min(board[1])
        maxx = np.max(board[0])
        maxy = np.max(board[1])

        for i in range(max(minx-1,0),min(maxx+2,self.size)):
            for j in range(max(miny-1,0),min(maxy+2,self.size)):
                if boardMatrix[i][j] == (1 if ForX else -1):
                    #2. Đếm...
                    consecutive += 1
                # gặp ô trống
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        # Ra: Ô trống ở cuối sau khi đếm. Giảm block rồi bắt đầu tính điểm sau đó reset lại ban đầu
                        blocks -= 1
                        score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else :
                        # 1. Vào reset lại blocks = 1 rồi bắt đầu đếm
                        blocks = 1
                #gặp quân địch
                elif consecutive > 0:
                    # 2.Ra:  Ô bị chặn sau khi đếm. Tính điểm sau đó reset lại.
                    score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else :
                    #1. Vào: reset lại blocks = 2 rồi bắt đầu đếm
                    blocks = 2
            # 3. Ra: nhưng lúc này đang ở cuối. Nếu liên tục thì vẫn tính cho đến hết dòng 
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
            # reset lại để tiếp tục chạy cho dòng tiếp theo
            consecutive = 0
            blocks = 2
        return score

    def evaluateVertical(self,boardMatrix,ForX,playersTurn ) :
        consecutive = 0
        blocks = 2
        score = 0
        board = np.array(boardMatrix)
        board = np.where(board != 0)
        minx = np.min(board[0])
        miny = np.min(board[1])
        maxx = np.max(board[0])
        maxy = np.max(board[1])
        for j in range(max(miny-1,0),min(maxy+2,self.size)):
            for i in range(max(minx-1,0),min(maxx+2,self.size)):
                if boardMatrix[i][j] == (1 if ForX else -1):
                    #2. Đếm...
                    consecutive += 1
                # gặp ô trống
                elif boardMatrix[i][j] == 0:
                    if consecutive > 0:
                        # Ra: Ô trống ở cuối sau khi đếm. Giảm block rồi bắt đầu tính điểm sau đó reset lại ban đầu
                        blocks -= 1
                        score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                        consecutive = 0
                        blocks = 1
                    else :
                        # 1. Vào reset lại blocks = 1 rồi bắt đầu đếm
                        blocks = 1
                #gặp quân địch
                elif consecutive > 0:
                    # 2.Ra:  Ô bị chặn sau khi đếm. Tính điểm sau đó reset lại.
                    score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                    consecutive = 0
                    blocks = 2
                else :
                    #1. Vào: reset lại blocks = 2 rồi bắt đầu đếm
                    blocks = 2
            # 3. Ra: nhưng lúc này đang ở cuối. Nếu liên tục thì vẫn tính cho đến
            if consecutive > 0:
                score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
            # reset lại để tiếp tục chạy cho dòng tiếp theo
            consecutive = 0
            blocks = 2
        return score

    def evaluateDiagonal(self, boardMatrix, ForX, playersTurn):
        score = 0
        consecutive = 0
        blocks = 2
        board = np.array(boardMatrix)
        board = np.where(board != 0)
        minx = max(np.min(board[0])-1,0)
        miny = max(np.min(board[1])-1,0)
        maxx = min(np.max(board[0])+1,self.size)
        maxy = min(np.max(board[1])+1,self.size)
        xx = maxx-minx + 1
        yy = maxy-miny + 1 
        l = xx + yy
        # Đường chéo /
        for k in range(0, l):
            iStart = max(0, k - yy + 1) + minx
            iEnd = min(min(xx,yy) - 1, k) + minx
            for i in range(iStart, iEnd + 1):
                j = k - i + minx + miny
                if(j<self.size and j>= 0):
                    if boardMatrix[i][j] == (1 if ForX else -1):
                        consecutive += 1    
                    elif boardMatrix[i][j] == 0:
                        if consecutive > 0:
                            blocks -= 1
                            score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                            consecutive = 0
                            blocks = 1
                        else:
                            blocks = 1
                    else:
                        if consecutive > 0:
                            score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                            consecutive = 0
                            blocks = 2
                        else:
                            blocks = 2
            if(consecutive > 0):
                score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
            consecutive = 0
            blocks = 2
        # Đường chéo \
        for k in range(1 - len(boardMatrix), len(boardMatrix)):
            iStart = max(0, k)
            iEnd = min(len(boardMatrix) + k - 1, len(boardMatrix) - 1)
            for i in range(iStart, iEnd + 1):
                j = i - k
                if(j<self.size and j>= 0):
                    if boardMatrix[i][j] == (1 if ForX else -1):
                        consecutive += 1
                    elif boardMatrix[i][j] == 0:
                        if consecutive > 0:
                            blocks -= 1
                            score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                            consecutive = 0
                            blocks = 1
                        else:
                            blocks = 1
                    else:
                        if consecutive > 0:
                            score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
                            consecutive = 0
                            blocks = 2
                        else:
                            blocks = 2
            if(consecutive > 0):
                score += self.getConsecutiveSetScore(consecutive, blocks, ForX == playersTurn)
            consecutive = 0
            blocks = 2
        return score
    
    # Tính điểm thế trận
    def getScore(self, boardMatrix, ForX, playersTurn):
        score = 0
        score += self.evaluateHorizontal(boardMatrix, ForX, playersTurn)
        score += self.evaluateVertical(boardMatrix, ForX, playersTurn)
        score += self.evaluateDiagonal(boardMatrix, ForX, playersTurn)
        return score

    def addNParray(self, nparray, nparray2):
        if np.size(nparray) == 0:
            nparray=np.array([nparray2])
        elif not (nparray2 in nparray.tolist()):
            nparray=np.append(nparray,[nparray2],axis=0)
        return nparray
    
    # Tìm những ô trống xung quanh XO
    def generateMoves(self, boardMatrix) :
        moveList = np.array([])
        boardSize = self.size
        borad = np.array(boardMatrix)
        borad = np.where(borad != 0)
        if np.size(borad) > 0:
            for i in range(len(borad[0])):
                x = borad[0][i]
                y = borad[1][i]
                if x > 0:
                    if y > 0:
                        if boardMatrix[x-1][y-1] == 0 :
                            moveList = self.addNParray(moveList,[x-1,y-1])
                    if y < boardSize-1:
                        if boardMatrix[x-1][y+1] == 0 :
                            moveList = self.addNParray(moveList,[x-1,y+1])
                    if boardMatrix[x-1][y] == 0:
                        moveList = self.addNParray(moveList,[x-1,y])
                if x < boardSize-1:
                    if y > 0:
                        if boardMatrix[x+1][y-1] == 0:
                            moveList = self.addNParray(moveList,[x+1,y-1])
                    if y < boardSize-1:
                        if boardMatrix[x+1][y+1] == 0 :
                            moveList = self.addNParray(moveList,[x+1,y+1])
                    if boardMatrix[x+1][y] == 0:
                        moveList = self.addNParray(moveList,[x+1,y])
                if y > 0:
                    if boardMatrix[x][y-1] == 0:
                        moveList = self.addNParray(moveList,[x,y-1])
                if y < boardSize-1:
                    if boardMatrix[x][y+1] == 0:
                        moveList = self.addNParray(moveList,[x,y+1])
        return moveList

    # Tính tỉ lệ điểm bot và ng chơi
    def evaluateBoardForWhite(self, boardMatrix, playersTurn):
        blackScore = self.getScore(boardMatrix, True, playersTurn)
        whiteScore = self.getScore(boardMatrix, False, playersTurn)
        if blackScore == 0:
            return whiteScore
        return whiteScore / blackScore

    # Tạo ra bàn cờ giả sử lượt đánh
    def playNextMove(self, board, move, isX):
        dummyBoard = copy.deepcopy(board)
        dummyBoard[move[0]][move[1]]= 1 if isX else -1
        return dummyBoard

    # Thuật toán minimax
    def minimaxSearchAB(self, depth, board, max, alpha, beta):
        if depth == 0:
            return [self.evaluateBoardForWhite(board, not max), None, None]
        # Danh sách nước đi
        moves = self.generateMoves(board)
        if len(moves) == 0:
            return [self.evaluateBoardForWhite(board, not max), None, None]
        bestMove = [0, 0, 0]
        if max:
            bestMove[0] = -1.0
            for move in moves:
                # Chơi thử với move hiện tại
                dummyBoard = self.playNextMove(board, move, False)
                tempMove = self.minimaxSearchAB(depth-1, dummyBoard, not max, alpha, beta)
                # Cập nhật alpha
                if ((tempMove[0]) > alpha) :
                    alpha = (tempMove[0])
				# Cắt tỉa beta
                if ((tempMove[0]) >= beta) :
                    return tempMove
                # Cập nhật bestMove
                if ((tempMove[0]) > bestMove[0]) :
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
        else:
            bestMove[0] = 100000000.0
            bestMove[1] = moves[0][0]
            bestMove[2] = moves[0][1]
            for move in moves:
                dummyBoard = self.playNextMove(board, move, True)
                tempMove = self.minimaxSearchAB(depth-1, dummyBoard, not max, alpha, beta)
                # Cập nhật beta
                if ((tempMove[0]) < beta) :
                    beta = (tempMove[0])
                # Cắt tỉa alpha
                if ((tempMove[0]) <= alpha) :
                    return tempMove
                if ((tempMove[0]) < bestMove[0]) :
                    bestMove = (tempMove)
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
        return bestMove

    # Tìm nước đi thắng của đối thủ để chặn
    def searchLoseMove(self, board):
        moves = self.generateMoves(board)
        losingMove = [None, None, None]
        if(self.player == True):
            for move in moves:
                dummyBoard = self.playNextMove(board, move, True)
                if self.getScore(dummyBoard, True, False) >= self.winScore:
                    losingMove[1] = move[0]
                    losingMove[2] = move[1]
                    return losingMove
            return losingMove
        else:
            for move in moves:
                dummyBoard = self.playNextMove(board, move, False)
                if self.getScore(dummyBoard, False, False) >= self.winScore:
                    losingMove[1] = move[0]
                    losingMove[2] = move[1]
                    return losingMove
            return losingMove

    # Tìm nước đi thắng
    def searchWinMove(self, board):
        moves = self.generateMoves(board)
        winningMove = [None, None, None]
        if(self.player == True):
            for move in moves:
                dummyBoard = self.playNextMove(board, move, False)
                if self.getScore(dummyBoard, False, False) >= self.winScore:
                    winningMove[1] = move[0]
                    winningMove[2] = move[1]
                    return winningMove
            return winningMove
        else:
            for move in moves:
                dummyBoard = self.playNextMove(board, move, True)
                if self.getScore(dummyBoard, True, False) >= self.winScore:
                    winningMove[1] = move[0]
                    winningMove[2] = move[1]
                    return winningMove
            return winningMove
    # Đề xuất lượt đánh cho bot
    def calcNextMove(self, board, depth):
        checkboard = np.array(board)
        checkboard = np.where(checkboard != 0)
        
        if(len(checkboard[0])==0):
            return (int(self.size/2),int(self.size/2))

        bestMove = self.searchWinMove(board)
        badMove = self.searchLoseMove(board)
        move = (0, 0)
        if bestMove[1] != None and bestMove[2] != None:
            move = (bestMove[1], bestMove[2])
        elif badMove[1] != None and badMove[2] != None:
            move = (badMove[1], badMove[2])
        else:
            bestMove = self.minimaxSearchAB(depth, board, True, -1.0, self.winScore)
            if bestMove[1] == None:
                move = None
            else:
                move = (bestMove[1], bestMove[2])
        return move