from copy import copy, deepcopy

import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout

puzzle = Puzzle(day=14, year=2021)

# data = """NNCB
#
# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C""".split('\n')

data = puzzle.input_data.split('\n')

pairs = {}
for ii in range(len(data[0]) - 1):
    p = data[0][ii:ii + 2]
    try:
        pairs[p] += 1
    except KeyError:
        pairs[p] = 1

rules = {}
for ln in data[2:]:
    in_0 = ln[0]
    in_1 = ln[1]
    ou = ln[-1]

    try:
        rules[in_0 + in_1]
        pyout()
    except KeyError:
        rules[in_0 + in_1] = [in_0 + ou, ou + in_1]


def step(old, rls):
    new = deepcopy(old)
    for rule in rls:
        try:
            occurrences = old[rule]
            new[rule] -= occurrences
        except KeyError:
            occurrences = 0

        for repl in rls[rule]:
            try:
                new[repl] += occurrences
            except KeyError:
                new[repl] = occurrences

    new = {key: new[key] for key in new if new[key] > 0}
    return new

for _ in range(40):
    pairs = step(pairs, rules)

quantities = {data[0][0]:1}
for pair in pairs:
    try:
        quantities[pair[1]] += pairs[pair]
    except KeyError:
        quantities[pair[1]] = pairs[pair]

max_ = max(quantities.values())
min_ = min([x for x in quantities.values() if x > 0])

# puzzle.answer_a = max_ - min_
puzzle.answer_b = max_ - min_

pyout()
