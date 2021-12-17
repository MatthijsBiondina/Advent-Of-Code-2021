import time
from copy import copy, deepcopy

import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout, plot

puzzle = Puzzle(day=17, year=2021)

# data = "9C0141080250320F1802104A08"
data = puzzle.input_data

tgt_x = (179, 201)
tgt_y = (-109, -63)

# x-velocity
xvel = [0, 201]
while xvel[0] * (xvel[0] + 1) / 2 < tgt_x[0]:
    xvel[0] += 1
pyout(xvel[0] * (xvel[0] + 1) / 2)

yvel = [tgt_y[0], -tgt_y[0]]

launch_x = np.arange(xvel[0], xvel[1] + 1, dtype=int)
launch_y = np.arange(yvel[0], yvel[1] + 1, dtype=int)

xvel = np.arange(xvel[0], xvel[1] + 1, dtype=int)
yvel = np.arange(yvel[0], yvel[1] + 1, dtype=int)

pos = np.zeros((yvel.shape[0], xvel.shape[0], 2), dtype=int)
tgt = np.zeros((yvel.shape[0], xvel.shape[0]), dtype=bool)

while np.any(pos[:, :, 1] >= tgt_y[0]):
    pos[..., 0] += xvel[None, :]
    pos[..., 1] += yvel[:, None]

    xvel = np.maximum(xvel - 1, 0)
    yvel -= 1

    A = tgt_x[0] <= pos[:, :, 0]
    B = pos[:, :, 0] <= tgt_x[1]
    C = tgt_y[0] <= pos[:, :, 1]
    D = pos[:, :, 1] <= tgt_y[1]
    tgt = np.where(A & B & C & D, True, tgt)

# reached = np.any(tgt, axis=1)
#
#
# ii = np.max(np.argwhere(reached)[:, 0])
# maxyvel = launch_y[ii]
#
# max_y_pos = maxyvel * (maxyvel + 1) // 2

puzzle.answer_b = np.sum(tgt)

pyout()
