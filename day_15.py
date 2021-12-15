import time
from copy import copy, deepcopy

import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout

puzzle = Puzzle(day=15, year=2021)

# data = """1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581""".split('\n')

data = puzzle.input_data.split('\n')
data = np.array([list(x) for x in data], dtype=int)

big = data.copy()
for ii in range(1, 5):
    big = np.concatenate((big, (data + ii - 1) % 9 + 1), axis=1)
data = big.copy()
for ii in range(1, 5):
    big = np.concatenate((big, (data + ii - 1) % 9 + 1), axis=0)
data = big

# print(data)
#
# def show_map()

def adjacent(x, include_self=False):
    ou = np.stack([np.full_like(x, sys.maxsize // 10) for _ in range(4)], axis=0)

    ou[0, 1:, :] = x[:-1, :]
    # ou[1, 1:, 1:] = x[:-1, :-1]
    ou[1, :, 1:] = x[:, :-1]
    # ou[3, :-1, 1:] = x[1:, :-1]
    ou[2, :-1, :] = x[1:, :]
    # ou[5, :-1, :-1] = x[1:, 1:]
    ou[3, :, :-1] = x[:, 1:]
    # ou[7, 1:, :-1] = x[:-1, 1:]

    return ou


M = np.full_like(data, fill_value=sys.maxsize // 10)
M[-1, -1] = 0
M_old = M.copy()

while True:

    M_new = np.min(adjacent(M_old + data), axis=0)

    M_new = np.minimum(M_new, M_old)

    if np.all(M_new == M_old):
        break
    else:
        M_old = M_new.copy()
M = M_old.copy()


puzzle.answer_b = M[0, 0]

# pyout()

pyout()
