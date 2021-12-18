import ast
import math
import time
from copy import copy, deepcopy

import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout, plot

puzzle = Puzzle(day=18, year=2021)
data = puzzle.input_data.split('\n')
# data = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
# [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
# [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
# [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
# [7,[5,[[3,8],[1,4]]]]
# [[2,[2,2]],[8,[8,1]]]
# [2,9]
# [1,[[[9,3],9],[[9,0],[0,7]]]]
# [[[5,[7,4]],7],1]
# [[[[4,2],2],6],[8,7]]""".split('\n')
# data = """[[[[4,3],4],4],[7,[[8,4],9]]]
# [1,1]""".split('\n')


def add(a, b):
    return f"[{a},{b}]"


def explode(a):
    r = 0
    ii_frm, ii_to = None, None
    values = ''
    struct = ''
    for ii in range(len(a)):
        if a[ii] == '[':
            r += 1
        elif a[ii] == ']':
            r -= 1
        if r > 4:
            ii_frm = ii
            jj = ii
            while a[jj] != ']':
                jj += 1
            ii_to = jj
            break

    if ii_frm is None:
        return a, False

    pair = ast.literal_eval(a[ii_frm: ii_to + 1])

    a = a[:ii_frm] + '0' + a[ii_to + 1:]
    II = ii_frm

    ii_frm, ii_to = None, None
    for ii in range(II + 1, len(a)):
        if a[ii] not in ('[', ',', ']'):
            ii_frm = ii
            for ii_to in range(ii_frm, len(a)):
                if a[ii_to] in ('[', ',', ']'):
                    break
            break
    if ii_frm is not None:
        a = f"{a[:ii_frm]}{int(a[ii_frm:ii_to]) + pair[1]}{a[ii_to:]}"

    ii_frm, ii_to = None, None
    for ii in range(II - 1, -1, -1):
        if a[ii] not in ('[', ',', ']'):
            ii_to = ii
            for ii_frm in range(ii_to, -1, -1):
                if a[ii_frm] in ('[', ',', ']'):
                    break
            ii_to += 1
            ii_frm += 1
            break

    if ii_frm is not None:
        a = f"{a[:ii_frm]}{int(a[ii_frm:ii_to]) + pair[0]}{a[ii_to:]}"

    return a, True

def split(a):
    frm, to_ = None, None
    for ii in range(len(a)):
        if a[ii] not in ('[', ',', ']'):
            frm = ii
            for to_ in range(frm, len(a)):
                if a[to_] in ('[', ',', ']'):
                    break
            if int(a[frm:to_]) > 9:
                break
            else:
                frm, to_ = None, None

    if frm is None:
        return a, False

    val = int(a[frm:to_])
    pair = f"[{math.floor(val/2)},{math.ceil(val/2)}]"
    a = f"{a[:frm]}{pair}{a[to_:]}"
    return a, True

def magnitude(a):
    if type(a) is str:
        return magnitude(ast.literal_eval(a))
    elif type(a) is list:
        return 3*magnitude(a[0]) + 2*magnitude(a[1])
    else:
        return a



while len(data) >= 2:
    in1 = data.pop(0)
    in2 = data.pop(0)
    ou = add(in1, in2)

    while True:
        ou, exploded = explode(ou)
        if exploded:
            continue

        ou, splitted = split(ou)
        if not splitted:
            break

    data.insert(0, ou)

data = data[0]

M = magnitude(ast.literal_eval(data))
puzzle.answer_a = M

max_magnitude = 0
for ii in tqdm(range(len(data))):
    for jj in range(len(data)):
        if ii != jj:
            a = data[ii]
            b = data[jj]

            ou = add(a, b)

            while True:
                ou, exploded = explode(ou)
                if exploded:
                    continue

                ou, splitted = split(ou)
                if not splitted:
                    break

            max_magnitude = max(max_magnitude, magnitude(ou))

puzzle.answer_b = max_magnitude


