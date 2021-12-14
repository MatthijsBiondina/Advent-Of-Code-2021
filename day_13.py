import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout

puzzle = Puzzle(day=13, year=2021)

data = puzzle.input_data.split('\n')
# data = """6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0
#
# fold along y=7
# fold along x=5"""
# data = data.split('\n')


def read_data(in_):
    dot_args = []
    instructions = []

    for line in in_:
        if line == '':
            continue
        try:
            line = line.split(',')
            dot_args.append([int(x) for x in line])
        except ValueError:
            instructions.append(line[0].split(' ')[-1])

    return np.array(dot_args, dtype=int), instructions


def init_paper(dots):
    xmax, ymax = np.max(dots, axis=0)

    P = np.zeros((ymax + 1, xmax + 1), dtype=bool)
    for x, y in dots:
        P[y, x] = True

    return P


def foldX(p: np.ndarray, col: int):
    slice_l = p[:, :col]
    slice_r = p[:, col + 1:][:, ::-1]

    if slice_l.shape[1] >= slice_r.shape[1]:
        frm = -slice_r.shape[1]
        slice_l[:, frm:] = slice_l[:, frm:] | slice_r
        return slice_l
    else:
        frm = -slice_l.shape[1]
        slice_r[:, frm:] = slice_r[:, frm:] | slice_l
        return slice_r


def foldY(p: np.ndarray, row: int):
    slice_u = p[:row, :]

    slice_d = p[row + 1:, :]
    slice_d = slice_d[::-1]

    if slice_u.shape[0] >= slice_d.shape[0]:
        frm = -slice_d.shape[0]
        slice_u[frm:] = slice_u[frm:] | slice_d
        return slice_u
    else:
        frm = -slice_u.shape[0]
        slice_d[frm:] = slice_d[frm:] | slice_u
        return slice_d


def fold(p: np.ndarray, instr: str):
    if instr[0] == 'x':
        col = int(instr.split('=')[-1])
        p = foldX(p, col)
    else:
        row = int(instr.split('=')[-1])
        p = foldY(p, row)
    return p


dot_coordinates, folds = read_data(data)
paper = init_paper(dot_coordinates)

for fld in folds:
    paper = fold(paper, fld)

n_dots = np.sum(paper)
# puzzle.answer_a = n_dots

pyout()
