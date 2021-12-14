import numpy as np
from aocd.models import Puzzle

from tools import pyout

puzzle = Puzzle(day=4, year=2021)

data = puzzle.input_data
while '  ' in data:
    data = data.replace('  ', ' ')
data = data.split('\n\n')
numbers, boards = data[0], data[1:]
boards = [board.split('\n') for board in boards]

b = []
for board in boards:
    b.append([])
    for row in board:
        b[-1].append([])
        for val in row.split(' '):
            if val is not '':
                b[-1][-1].append(int(val))

boards = np.array(b)
b0 = boards[0]

bingo = np.zeros(boards.shape, dtype=bool)

for nr in numbers.split(','):


    nr = int(nr)

    A = boards == nr
    bingo = np.where(boards == nr, True, bingo)

    rows = bingo.astype(int).sum(axis=2)
    rows = rows == 5
    rows = np.any(rows, axis=1)

    if np.any(rows):
        if boards.shape[0] == 1:
            break

        msk = np.zeros(boards.shape[0], dtype=bool)
        winning_index = np.argwhere(rows).squeeze(1)
        msk[winning_index] = True

        boards = boards[~ msk]
        bingo = bingo[~ msk]

        # pyout()


    cols = bingo.astype(int).sum(axis=1)
    cols = cols == 5
    cols = np.any(cols, axis=1)

    if np.any(cols):
        if boards.shape[0] == 1:
            break

        msk = np.zeros(boards.shape[0], dtype=bool)
        winning_index = np.argwhere(cols).squeeze(1)
        msk[winning_index] = True
        boards = boards[~ msk]
        bingo = bingo[~ msk]


board = boards[0]
bingo = bingo[0]

unm = np.sum(board[~ bingo])
puzzle.answer_b = unm * nr

pyout()
