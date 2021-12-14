import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm

from tools import pyout

puzzle = Puzzle(day=6, year=2021)

data = puzzle.input_data

F = np.array(data.split(','), dtype=int)

nr = lambda x: np.sum(F == x)

fish = np.array([nr(0), nr(1), nr(2), nr(3), nr(4), nr(5), nr(6), nr(7), nr(8)])

for _ in tqdm(range(256)):
    fish = np.roll(fish, -1)
    fish[6] += fish[-1]

nr_of_fish = np.sum(fish)

puzzle.answer_b = nr_of_fish

pyout()
