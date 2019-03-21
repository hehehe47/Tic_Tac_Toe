def helper(l, n):
    # length = len(l)
    # for i in range(length-n+1):
    #     temp = l[i]
    #     for j in range(n):
    #         if i+j>length or l[i+j] != temp:
    #             return False
    #             break;
    #     return True
    return True


def score(l):
    sum = 0
    length = len(l)
    i = 0
    while i < length:
        temp = l[i]
        if temp == '-':
            i += 1
            continue
        else:
            j = 0
            while i + j < length and l[i + j] == temp:
                j += 1
            count = j
            if temp == 'x':
                sum += 10 ** (count - 1)
            else:
                sum += -10 ** (count - 1)
            i += count
    return sum


def evaluation_Function(board, n):
    sum = 0
    length = len(board)
    for row in board:
        bool = helper(row, n)
        if bool:
            sum += score(row)

    for i in range(length):
        column = [row[i] for row in board]
        bool = helper(column, n)
        if bool:
            sum += score(column)

    for i in range(n - 1, length):
        l1 = []
        for j in range(i + 1):
            l1.append(board[j][i - j])
        bool = helper(l1, n)
        if bool:
            sum += score(l1)
    for i in range(1, length - n + 1):
        l1 = []
        for j in range(i, length):
            l1.append(board[j][length - j + i - 1])
        bool = helper(l1, n)
        if bool:
            sum += score(l1)
    for i in range(0, length - n + 1):
        l1 = []
        for j in range(length - i):
            l1.append(board[i + j][j])
        bool = helper(l1, n)
        if bool:
            sum += score(l1)
    for i in range(1, length - n + 1):
        l1 = []
        for j in range(length - i):
            l1.append(board[j][i + j])
        bool = helper(l1, n)
        if bool:
            sum += score(l1)

    return sum
