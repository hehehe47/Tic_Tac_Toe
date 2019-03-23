import sys


# score is a value by 10's exponential time
# one in a row is 1
# two in a row is 10
# three in a row is 100
def score(l, n):
    score = 0
    for i in range(len(l) - n + 1):
        temp = 0
        count = 0
        for j in range(n):
            cell = l[i + j]
            if cell == '-':
                count = 0
            elif cell == 'X' and temp >= 0:
                count += 1
                temp += 10 ** count
            elif cell == 'O' and temp <= 0:
                count += 1
                temp -= 10 ** count
            else:
                temp = 0
                break
        score += temp
    return score


# any blank to move?
def ismoveleft(board):
    for row in board:
        for cell in row:
            if cell == '-':
                return True
    return False


# anybody has won?
def checkstatus(board, n):
    if not ismoveleft(board):
        print('Draw')
        exit()
    utility = evaluation_Function(board, n)
    if utility > 10 ** n:
        print('X wins')
        exit()
    elif utility < -10 ** n:
        print('O wins')
        exit()


# evaluate the whole board
# by adding row's, column's and diagonal’s total score
def evaluation_Function(board, n):
    sum = 0
    length = len(board)
    for row in board:
        utility = score(row, n)
        if abs(utility) > 10 ** n:
            return utility
        sum += utility

    for i in range(length):
        column = [row[i] for row in board]
        utility = score(column, n)
        if abs(utility) > 10 ** n:
            return utility
        sum += utility

    for i in range(n - 1, length):
        l1 = []
        for j in range(i + 1):
            l1.append(board[j][i - j])
        utility = score(l1, n)
        if abs(utility) > 10 ** n:
            return utility
        sum += utility
    for i in range(1, length - n + 1):
        l1 = []
        for j in range(i, length):
            l1.append(board[j][length - j + i - 1])
        utility = score(l1, n)
        if abs(utility) > 10 ** n:
            return utility
        sum += utility
    for i in range(0, length - n + 1):
        l1 = []
        for j in range(length - i):
            l1.append(board[i + j][j])
        utility = score(l1, n)
        if abs(utility) > 10 ** n:
            return utility
        sum += utility
    for i in range(1, length - n + 1):
        l1 = []
        for j in range(length - i):
            l1.append(board[j][i + j])
        utility = score(l1, n)
        if abs(utility) > 10 ** n:
            return utility
        sum += utility
    return sum


# minimax function
def minimax(board, n, depth, ismax, a, b):
    utility = evaluation_Function(board, n)
    # limit depth
    # if utility means game ends, just return
    if depth >= 2 or utility >= 10 ** n or utility <= -10 ** n:
        return utility - 10 * depth
    # if no blanks, just return
    if not ismoveleft(board):
        return False

    # max function
    if ismax:
        best = -sys.maxsize
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, n, depth + 1, False, a, b))
                    board[i][j] = '-'
                    if best >= b:
                        return best
                    a = max(a, best)
        return best

    # min function
    else:
        best = sys.maxsize
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, n, depth + 1, True, a, b))
                    board[i][j] = '-'
                    if best <= a:
                        return best
                    b = min(b, best)
        return best


# find the best move for player ‘X’
def findmax(board, n):
    best = -sys.maxsize
    row = -1
    column = -1
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '-':
                board[i][j] = 'X'
                utility = minimax(board, n, 1, False, -sys.maxsize, sys.maxsize)
                board[i][j] = '-'
                if utility >= best:
                    row = i
                    column = j
                    best = utility

    board[row][column] = 'X'
    # check if either player has won
    # if won, whole program exit
    checkstatus(board, n)
    return row, column


# find the best move for player ‘O’
def findmin(board, n):
    best = sys.maxsize
    row = -1
    column = -1
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '-':
                board[i][j] = 'O'
                utility = minimax(board, n, 1, True, -sys.maxsize, sys.maxsize)
                board[i][j] = '-'
                if utility <= best:
                    row = i
                    column = j
                    best = utility

    board[row][column] = 'O'
    # check if either player has won
    # if won, whole program exit
    checkstatus(board, n)
    return row, column
