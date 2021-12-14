from aocd.models import Puzzle
import numpy as np

from tools import pyout

puzzle = Puzzle(year=2021, day=3)
data = puzzle.input_data.split('\n')

data = np.array([[x for x in y] for y in data]).astype(int)
data = np.where(data == 0, -1, data)

gdata = data.copy()
for ii in range(data.shape[1]):
    bit = 1 if np.sum(gdata[:, ii]) >= 0 else -1
    gdata = gdata[gdata[:, ii] == bit]

    if gdata.shape[0] == 1:
        break
gdata = gdata[0]

edata = data.copy()
for ii in range(data.shape[1]):
    bit = -1 if np.sum(edata[:, ii]) >= 0 else 1
    edata = edata[edata[:, ii] == bit]

    if edata.shape[0] == 1:
        break
edata = edata[0]


pyout()

# data = np.sum(data, axis=0)

gdata = (gdata > 0)
gamma = ''.join(list(gdata.astype(int).astype(str)))

edata = (edata > 0)
epsil = ''.join(list(edata.astype(int).astype(str)))

gamma = int(gamma, 2)
epsil = int(epsil, 2)

puzzle.answer_b = gamma * epsil

pyout()
