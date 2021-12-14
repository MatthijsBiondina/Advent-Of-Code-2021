import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm

from tools import pyout

puzzle = Puzzle(day=9, year=2021)

data = np.array([list(x) for x in puzzle.input_data.split('\n')], dtype=int)

ou = np.ones_like(data).astype(bool)

ou[1:, :] = ou[1:, :] & (data[1:, :] < data[:-1, :])
ou[:-1, :] = ou[:-1, :] & (data[:-1, :] < data[1:, :])
ou[:, 1:] = ou[:, 1:] & (data[:, 1:] < data[:, :-1])
ou[:, :-1] = ou[:, :-1] & (data[:, :-1] < data[:, 1:])

ii = np.argwhere(ou)

risk = data[ii[:, 0], ii[:, 1]] + 1
risk = np.sum(risk)

lake = np.ones_like(data)
lake = np.where(data == 9, 0, lake)

basins = []
while True:
    ii = np.argwhere(lake)
    if ii.shape[0] == 0:
        break
    else:
        ii = ii[0]

    lake_new = lake.copy()
    lake_new[ii[0], ii[1]] = 2
    lake_old = None

    while True:
        lake_old = lake_new.copy()

        lake_new[1:, :] = np.where(lake_new[1:, :] > 0,
                                   np.maximum(lake_new[1:, :], lake_new[:-1, :]),
                                   lake[1:, :])
        lake_new[:-1, :] = np.where(lake_new[:-1, :] > 0,
                                    np.maximum(lake_new[:-1, :], lake_new[1:, :]),
                                    lake[:-1, :])
        lake_new[:, 1:] = np.where(lake_new[:, 1:] > 0,
                                   np.maximum(lake_new[:, 1:], lake_new[:, :-1]),
                                   lake[:, 1:])
        lake_new[:, :-1] = np.where(lake_new[:, :-1] > 0,
                                    np.maximum(lake_new[:, :-1], lake_new[:, 1:]),
                                    lake[:, :-1])
        lake_new = np.maximum(lake_new, lake_old)

        if np.all(lake_new == lake_old):
            break


    found_basin = (lake_new == 2)

    lake[found_basin] = 0
    basins.append(np.sum(found_basin.astype(int)))

basins = sorted(basins, reverse=True)

puzzle.answer_b = basins[0] * basins[1] * basins[2]

pyout()
