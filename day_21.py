import ast
import math
import time
from copy import copy, deepcopy
import torch
import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys
import torch.nn.functional as F
from tools import pyout, plot

puzzle = Puzzle(day=21, year=2021)

data = puzzle.input_data
# data = """Player 1 starting position: 4
# Player 2 starting position: 8"""

pos_1 = int(data.split('\n')[0].split(' ')[-1]) - 1
pos_2 = int(data.split('\n')[1].split(' ')[-1]) - 1

state = np.zeros((10, 10, 22, 22), dtype=int)
state[pos_1, pos_2, 0, 0] = 1

pos = np.zeros((10, 10), dtype=int)
score = np.zeros((22, 22), dtype=int)

combinations = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
# combinations = {1: 1}


def roll(A, B, axis):
    for val, qty in combinations.items():
        A += np.roll(B * qty, val, axis=axis)


while np.any(state[:, :, :21, :21] > 0):
    new_state = np.zeros_like(state)

    for val, qty in combinations.items():
        new_state[:, :, :21, :21] += np.roll((state * qty)[:, :, :21, :21], val, axis=0)

    new_state[:, :, 21, :] += state[:, :, 21, :]
    new_state[:, :, :, 21] += state[:, :, :, 21]
    for ii in range(10):
        new_state[ii, :, 21, :21] += np.sum(new_state[ii, :, (21 - ii - 1): 21, :21], axis=1)
        new_state[ii, :, ii + 1:21, :21] = new_state[ii, :, :21 - ii - 1, :21]
        new_state[ii, :, :ii + 1, :21] = 0

    state = new_state.copy()
    pos = np.sum(state[:, :, :21, :21], axis=(2, 3))
    score = np.sum(state, axis=(0, 1))
    # pyout()

    new_state = np.zeros_like(state)
    # if np.any(state[:, :, 21, :] > 0):
    #     pyout()

    for val, qty in combinations.items():
        new_state[:, :, :21, :21] += np.roll((state * qty)[:, :, :21, :21], val, axis=1)

    new_state[:, :, 21, :] += state[:, :, 21, :]
    new_state[:, :, :, 21] += state[:, :, :, 21]
    for ii in range(10):
        new_state[:, ii, :21, 21] += np.sum(new_state[:, ii, :21, 21 - ii - 1:21], axis=2)
        new_state[:, ii, :21, ii + 1:21] = new_state[:, ii, :21, :21 - ii - 1]
        new_state[:, ii, :21, :ii + 1] = 0
    A = np.argwhere(new_state)
    state = new_state.copy()
    pos = np.sum(state[:, :, :21, :21], axis=(2, 3))
    score = np.sum(state, axis=(0, 1))
    # pyout()

wins_1 = np.sum(state[:, :, 21, :21])
wins_2 = np.sum(state[:, :, :21, 21])

score = max(wins_1, wins_2)
puzzle.answer_b = score

# pyout()
