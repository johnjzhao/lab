import os
import sys
from collections import deque
from itertools import product

def coinOnTheTable(m, k, board):
    m = len(board)
    n = len(board[0])

    def is_inside(x, y):
        return 0 <= x < m and 0 <= y < n

    distances = {}
    q = deque()
    q.append(((0, 0, 0), 0))
    while len(q) > 0:
        (z, i, j), d = q.pop()
        if not is_inside(i, j) or d > k:
            continue
        if (z, i, j) in distances:
            continue
        distances[(z, i, j)] = d
        if board[i][j] == '*':
            continue
        q.append(((z + int(board[i][j] != 'U'), i - 1, j), d + 1))
        q.append(((z + int(board[i][j] != 'D'), i + 1, j), d + 1))
        q.append(((z + int(board[i][j] != 'L'), i, j - 1), d + 1))
        q.append(((z + int(board[i][j] != 'R'), i, j + 1), d + 1))

    special_i, special_j = next((i, j) for i, j in product(range(m), range(n))
                                if board[i][j] == '*')
    for z in range(k + 1):
        state = (z, special_i, special_j)
        if state in distances and distances[state] <= k:
            return z
    return -1

if __name__ == '__main__':
    
    NMK = input().strip()

    n = int(NMK.split(' ')[0])
    m = int(NMK.split(' ')[1])
    k = int(NMK.split(' ')[2])

    board = []

    for _ in range(n):
        board_item = input()
        board.append(board_item)

    result = coinOnTheTable(m, k, board)
    print(result)
