import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm

from tools import pyout

puzzle = Puzzle(day=10, year=2021)

data = puzzle.input_data

syntax_values = {')': 1, ']': 2, '}': 3, '>': 4}

closing_bracks = {'(': ')', '[': ']', '{': '}', '<': '>'}

all_scores = []
for line in data.split('\n'):
    bracks = []
    corrupt = False
    for c in line:
        if c in ['(', '[', '{', '<']:

            bracks.append(c)
        else:
            if c == closing_bracks[bracks[-1]]:
                del bracks[-1]
            else:
                corrupt = True
                break
    if not corrupt:
        complete = [closing_bracks[c] for c in bracks[::-1]]

        score = 0
        for c in complete:
            score *= 5
            score += syntax_values[c]
        all_scores.append(score)

all_scores = sorted(all_scores)
score = int(np.median(all_scores))

puzzle.answer_b = score
pyout()

# puzzle.answer_a = score
pyout()

pyout()
