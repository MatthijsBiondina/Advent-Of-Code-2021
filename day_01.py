from aocd.models import Puzzle
import numpy as np

puzzle = Puzzle(year=2021, day=1)

data = np.array(list(int(x) for x in puzzle.input_data.split('\n')))

windows = np.sum(np.stack((data[0:-2], data[1:-1], data[2:]), axis=1), axis=1)

incr = np.sum((windows[1:] > windows[:-1]).astype(int))

puzzle.answer_b = incr

print()
