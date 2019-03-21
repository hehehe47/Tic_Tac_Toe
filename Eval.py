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
        score += temp
    return score


def ismoveleft(board):
    for row in board:
        for cell in row:
            if cell == '-':
                return True
    return False


def evaluation_Function(board, n):
    sum = 0
    length = len(board)
    for row in board:
        utility = score(row, n)
        sum += utility

    for i in range(length):
        column = [r[i] for r in board]
        utility = score(column, n)
        sum += utility

    for i in range(n - 1, length):
        l1 = []
        for j in range(i + 1):
            l1.append(board[j][i - j])
        utility = score(l1, n)
        sum += utility
    for i in range(1, length - n + 1):
        l1 = []
        for j in range(i, length):
            l1.append(board[j][length - j + i - 1])
        utility = score(l1, n)
        sum += utility
    for i in range(0, length - n + 1):
        l1 = []
        for j in range(length - i):
            l1.append(board[i + j][j])
        utility = score(l1, n)
        sum += utility
    for i in range(1, length - n + 1):
        l1 = []
        for j in range(length - i):
            l1.append(board[j][i + j])
        utility = score(l1, n)
        sum += utility
    return sum


def minimax(board, n, depth, ismax, a, b):
    utility = evaluation_Function(board, n)

    if depth > 2 or utility >= 10 ** n or utility <= -10 ** n:
        return utility
    if not ismoveleft(board):
        return False

    if ismax:
        best = -sys.maxsize
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    board[i][j] = 'X'

                    best = max(best, minimax(board, n, depth + 1, not ismax, a, b))
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
                    best = min(best, minimax(board, n, depth + 1, ismax, a, b))
                    board[i][j] = '-'
                    if best <= a:
                        return best
                    b = min(b, best)
        return best


def findbestmove(board, n, ismax):
    best = -sys.maxsize
    row = -1
    column = -1

    if ismax:
        player = 'X'
    else:
        player = 'O'

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '-':
                board[i][j] = player
                utility = minimax(board, n, 0, not ismax, -10000, 10000)
                board[i][j] = '-'
                if utility > best:
                    row = i
                    column = j
                    best = utility
    return (row, column)
