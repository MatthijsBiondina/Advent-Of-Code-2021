import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm

from tools import pyout

puzzle = Puzzle(day=7, year=2021)

data = puzzle.input_data
data = list(np.array(data.split(','), dtype=int))

pos = list(set(data))
N = np.array([data.count(ii) for ii in pos])

now_pos = np.array(pos)
tgt_pos = np.arange(min(pos), max(pos) + 1)

now_pos = now_pos[None, :]
tgt_pos = tgt_pos[:, None]

dmatrix = np.sum(np.abs(tgt_pos - now_pos) * N[None, :], axis=1)

bestpos = np.argmin(dmatrix)
fuel = dmatrix[bestpos]

# puzzle.answer_a = fuel

dist = np.abs(tgt_pos - now_pos)

cmtrx = np.empty_like(dist)
cost = 0
for steps in range(np.max(dist)+1):
    cost += steps
    cmtrx = np.where(dist == steps, cost, cmtrx)

cmtrx *= N
cmtrx = np.sum(cmtrx, axis=1)
bestpos = np.argmin(cmtrx)
fuel = cmtrx[bestpos]

# puzzle.answer_b = fuel



pyout()
