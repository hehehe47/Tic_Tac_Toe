import sys


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


def ismoveleft(board):
    for row in board:
        for cell in row:
            if cell == '-':
                return True
    return False


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


def minimax(board, n, depth, ismax, a, b):
    utility = evaluation_Function(board, n)

    if depth >= 2 or utility >= 10 ** n or utility <= -10 ** n:
        return utility - 10 * depth
    if not ismoveleft(board):
        return False

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
    checkstatus(board, n)
    return row, column


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
    checkstatus(board, n)
    return row, column

