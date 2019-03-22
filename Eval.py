import sys


def score(l, target):
    value = 0
    length = len(l)
    i = 0
    while i < length:
        if (l[i] == 'X'):
            cnt = 1
            blk = 0
            j = 1
            if (l[i - 1] == 'O' or i == 0):
                blk += 1
            while i + j < length and l[i + j] == 'X':
                cnt += 1
                j += 1
            i += j
            if (i >= length):
                blk += 1
            elif (l[i] == 'O'):
                blk += 1
            value += getValue(cnt, blk, target)
        i += 1
        if value == 10 ** target:
            print(l)
            print('end')
            exit(0)

    return value


def getValue(cnt, blk, target):
    # no block around the connect cnt
    if (blk == 0):
        return 10 ** cnt
    elif (blk == 1):
        return 10 ** (cnt - 1)
    else:
        if (cnt >= target):
            return 10 ** target
        else:
            return 0


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
    # utility = evaluation_Function(board, n)
    # utility =

    # if depth == 0 or utility >= 10 ** n or utility <= -10 ** n:
    if depth == 0:
        return evaluation_Function(board, n)
    if not ismoveleft(board):
        return False

    if ismax:
        best = -sys.maxsize
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '-':
                    board[i][j] = 'X'

                    best = max(best, minimax(board, n, depth - 1, not ismax, a, b))
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
                    best = min(best, minimax(board, n, depth - 1, ismax, a, b))
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
                utility = minimax(board, n, 2, not ismax, -float('inf'), float('inf'))
                board[i][j] = '-'
                if utility > best:
                    row = i
                    column = j
                    best = utility
    return (row, column)
