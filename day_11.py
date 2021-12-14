import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm

from tools import pyout

puzzle = Puzzle(day=11, year=2021)

# X = """5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526"""
X = np.array([list(x) for x in puzzle.input_data.split('\n')], dtype=int)

# X = np.array([[1, 1, 1, 1, 1],
#               [1, 9, 9, 9, 1],
#               [1, 9, 1, 9, 1],
#               [1, 9, 9, 9, 1],
#               [1, 1, 1, 1, 1]])

# X = np.array([list(x) for x in X.split('\n')], dtype=int)

def adjacent(x, include_self=False):
    ou = np.stack([np.zeros_like(x) for _ in range(8)], axis=0)

    ou[0, 1:, :] = x[:-1, :]
    ou[1, 1:, 1:] = x[:-1, :-1]
    ou[2, :, 1:] = x[:, :-1]
    ou[3, :-1, 1:] = x[1:, :-1]
    ou[4, :-1, :] = x[1:, :]
    ou[5, :-1, :-1] = x[1:, 1:]
    ou[6, :, :-1] = x[:, 1:]
    ou[7, 1:, :-1] = x[:-1, 1:]

    return ou




for ii in range(100000000):
    flashes = 0
    X += 1

    while np.any(X > 9):
        flashes += np.sum(X > 9)
        stimulated = np.where(X > 0,
                              np.sum(adjacent(X) > 9, axis=0),
                              0)
        X = np.where(X > 9, 0, X + stimulated)

    if flashes == 100:
        break

puzzle.answer_b = ii+1

pyout()
