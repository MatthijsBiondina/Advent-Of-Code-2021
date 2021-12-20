import ast
import math
import time
from copy import copy, deepcopy
from typing import Set

import cupy as np
import torch
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout, plot, poem

R = []
for xx in range(4):
    for yy in range(4):
        for zz in range(4):
            X = np.eye(3)
            for _ in range(xx):
                X = X @ np.array([[1, 0, 0],
                                  [0, 0, -1],
                                  [0, 1, 0]])
            for _ in range(yy):
                X = X @ np.array([[0, 0, 1],
                                  [0, 1, 0],
                                  [-1, 0, 0]])
            for _ in range(zz):
                X = X @ np.array([[0, -1, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]])

            if str(X) not in [str(x) for x in R]:
                R.append(X)
R = np.stack(R, axis=0).astype(int)

puzzle = Puzzle(day=19, year=2021)
data = puzzle.input_data
data = data.split('\n\n')
data = [d.split('\n')[1:] for d in data]
data = [[xyz.split(',') for xyz in d] for d in data]
data = [np.array(x, dtype=int) for x in data]


def align(S1: np.ndarray, S2: np.ndarray):

    scan1 = S1[1].copy()
    scan2 = S2[1].copy()

    # ROTATE
    scan2 = (R[:, None, :] @ scan2[None, :, :, None]).squeeze(-1)

    # TRANSLATE
    diff = (scan1[None, None, :, :] - scan2[:, :, None, :])
    scan2 = scan2[:, None, None, :, :] + (scan1[None, None, :, :] - scan2[:, :, None, :])[..., None, :]

    # COMPARE
    overl = (scan1[None, None, None, :, None, :] == scan2[:, :, :, None, :, :])
    overl = np.all(overl, axis=-1)
    overl = np.sum(overl, axis=(-1, -2))
    overl = np.argwhere(overl >= 12)

    if len(overl) > 0:
        ii = overl[0]
        diff = diff[ii[0], ii[1], ii[2]]
        scan2 = scan2[ii[0], ii[1], ii[2]]

        return True, (diff, scan2)
    else:
        return False, None


try:
    with open("res/day_19_scanners.txt", "r") as f:
        scanners = ast.literal_eval(f.read())

    scanners = np.array(list(scanners))
    dmatrix = scanners[None, :, :] - scanners[:, None, :]
    dmatrix = np.abs(dmatrix)
    dmatrix = np.sum(dmatrix, axis=-1)

    puzzle.answer_b = np.max(dmatrix)
except FileNotFoundError:
    data = [(np.array([0, 0, 0]), x) for x in data]

    fixed_done = []
    fixed_todo = [data[0]]
    unknown = data[1:]

    pbar = tqdm(total=len(data), desc=poem("Aligning Sensor Data"), leave=False)

    while len(fixed_todo) > 0:
        S1 = fixed_todo.pop(0)
        for ii in range(len(unknown) - 1, -1, -1):
            S2 = unknown[ii]
            overlap, realigned = align(S1, S2)
            if overlap:
                del unknown[ii]
                fixed_todo.append(realigned)

        fixed_done.append(S1)

        # scanners = [x[0] for x in fixed_done] + [x[0] for x in fixed_todo]

        pbar.update(1)

    scanners = []
    beacons: Set = set()
    for scanner in fixed_done:
        scanners.append(list(scanner[0]))
        for ii in range(scanner[1].shape[0]):
            beacons.add(tuple(scanner[1][ii].tolist()))

    # with open("res/day_19_scanners.txt", 'w+') as f:
    #     f.write(str(scanners))
    #
    # with open("res/day_19_scanners.txt", "r") as f:
    #     scanners = ast.literal_eval(f.read())

    scanners = np.array(list(scanners))
    dmatrix = scanners[None, :, :] - scanners[:, None, :]
    dmatrix = np.abs(dmatrix)
    dmatrix = np.sum(dmatrix, axis=-1)

    size = np.max(dmatrix)

    # puzzle.answer_b = np.max(dmatrix)
    # pyout(np.max(dmatrix))

    # pyout()
