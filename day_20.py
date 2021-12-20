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

puzzle = Puzzle(day=20, year=2021)

data = puzzle.input_data

# data = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
#
# #..#.
# #....
# ##..#
# ..#..
# ..###"""

data = data.replace('.', '0').replace('#', '1')
data = data.split('\n')

device = torch.device("cpu")

program = torch.tensor(np.array(list(data[0]), dtype=int), device=device)

img = torch.tensor(np.array([list(x) for x in data[2:]], dtype=int), device=device)
img = img[None, None, :, :]

filter = torch.tensor(np.array([[256, 128, 64],
                                [32, 16, 8],
                                [4, 2, 1]]), device=device)
filter = filter[None, None, :, :]

# plot(img[0,0].cpu().numpy())

for ii in tqdm(range(50)):
    pad = 2
    if ii % 2 == 1:
        img = F.pad(img, (pad,) * 4, value=1)
    else:
        img = F.pad(img, (pad,) * 4, value=0)

    II = F.conv2d(img, filter, padding=0)
    h, w = II.size(2), II.size(3)
    II = II.view(-1)
    img = program[II].view(1, 1, h, w)

plot(img[0, 0].cpu().numpy())

pixels = int(torch.sum(img).cpu().item())

puzzle.answer_b = pixels

# pyout()/
