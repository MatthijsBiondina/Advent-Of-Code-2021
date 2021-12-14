import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout

puzzle = Puzzle(day=12, year=2021)

data = puzzle.input_data.split('\n')

nodes = {}
for link in data:
    n0, n1 = link.split('-')
    try:
        nodes[n0].append(n1)
    except KeyError:
        nodes[n0] = [n1]

    try:
        nodes[n1].append(n0)
    except KeyError:
        nodes[n1] = [n0]

for n in nodes:
    nodes[n] = list(set(nodes[n]))

# find all paths
F = []
U = [['start']]
while len(U) > 0: # while unfinished paths left
    pth = U.pop(0)
    if pth[-1] == 'end': # if at end, paht is finished
        F.append(pth)
    else:
        for next_node in nodes[pth[-1]]: # all possible target nodes
            if next_node.upper() == next_node: # if big cave
                U.append(pth + [next_node])
            elif next_node not in pth:
                U.append(pth + [next_node])
            else:
                if next_node == 'start':
                    continue
                small_caves = [x for x in pth if x != 'start' and x != 'end' and x.lower() == x]

                if len(list(set(small_caves))) == len(small_caves):
                    U.append(pth + [next_node])
                # else:
                #     pyout()

                # or next_node not in pth:



puzzle.answer_b = len(F)
pyout()
