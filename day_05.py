import numpy as np
from aocd.models import Puzzle

from tools import pyout

puzzle = Puzzle(day=5, year=2021)
data = puzzle.input_data

in_ = data.split('\n')
frm = np.array([x.split(' -> ')[0].split(',') for x in in_], dtype=int)
to_ = np.array([x.split(' -> ')[1].split(',') for x in in_], dtype=int)

dim = max(np.max(frm), np.max(to_)) + 1
M = np.zeros((dim, dim), dtype=int)

for ii in range(frm.shape[0]):
    xf, xt = frm[ii,0], to_[ii,0]
    xr = np.arange(min(xf, xt), max(xf, xt) + 1)
    xr = xr if xf < xt else xr[::-1]



    yf, yt = frm[ii,1], to_[ii,1]
    yr = np.arange(min(yf, yt), max(yf, yt) + 1)
    yr = yr if yf < yt else yr[::-1]


    if xr.shape[0] > yr.shape[0]:
        yr = np.full_like(xr, frm[ii, 1])
    elif xr.shape[0] < yr.shape[0]:
        xr = np.full_like(yr, frm[ii, 0])

    M[xr, yr] += 1

# overlap = M > 1

overlap = np.sum((M > 1).astype(int))

puzzle.answer_b = overlap

pyout()
