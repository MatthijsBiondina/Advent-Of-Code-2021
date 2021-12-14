import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm

from tools import pyout

puzzle = Puzzle(day=8, year=2021)

data = puzzle.input_data.split('\n')


def mkdig(lst):
    return ''.join(sorted(lst))

N = 0
for line in data:
    # dig = line.replace(' | ',' ').split(' ')
    dig = line.split(' | ')[0].split(' ')

    # find top segment comparing one and seven
    n1 = [d for d in dig if len(d) == 2][0]
    n7 = [d for d in dig if len(d) == 3][0]
    s0 = [l for l in n7 if l not in n1][0]

    # find top right segment by seeing which is missing from six
    n069 = [d for d in dig if len(d) == 6]
    n6 = [d for d in n069 if not (n1[0] in d and n1[1] in d)][0]
    s2 = [l for l in n1 if l not in n6][0]
    # and bottom right segment is the other one that is in 6
    s5 = [l for l in n1 if l in n6][0]

    # with segments 2 and 5 we can find what input corresponds with 0
    # we can find 0 by comparing 0 and 9 with 4
    n09 = [d for d in n069 if d != n6]
    n4 = [d for d in dig if len(d) == 4][0]
    n0 = [d for d in n09 if len([l for l in d if l in n4]) == 3][0]


    # n0 = [d for d in n069 if s2 in d and s5 in d]

    # compare 0 and 8 to find middle segment
    n8 = [d for d in dig if len(d) == 7][0]
    s3 = [l for l in n8 if l not in n0][0]

    # we know all segments in 3 except bottom
    n235 = [d for d in dig if len(d) == 5]
    n3 = [d for d in n235 if (s2 in d and s5 in d)][0]
    s6 = [l for l in n3 if l not in (s0, s2, s3, s5)][0]

    # with 9 we can find the bottom left segment
    n9 = [d for d in n069 if d not in (n0, n6)][0]
    s4 = [l for l in n8 if l not in n9][0]

    # we know all but one
    s1 = [l for l in n8 if l not in (s0, s2, s3, s4, s5, s6)][0]

    d0 = mkdig([s0, s1, s2, s4, s5, s6])
    d1 = mkdig([s2, s5])
    d2 = mkdig([s0, s2, s3, s4, s6])
    d3 = mkdig([s0, s2, s3, s5, s6])
    d4 = mkdig([s1, s2, s3, s5])
    d5 = mkdig([s0, s1, s3, s5, s6])
    d6 = mkdig([s0, s1, s3, s4, s5, s6])
    d7 = mkdig([s0, s2, s5])
    d8 = mkdig([s0, s1, s2, s3, s4, s5, s6])
    d9 = mkdig([s0, s1, s2, s3, s5, s6])

    vals = {d0: 0, d1: 1, d2: 2, d3: 3, d4: 4, d5: 5, d6: 6, d7: 7, d8: 8, d9: 9}

    found = []
    for d in dig:
        try:
            found.append(vals["".join(sorted(d))])
        except:
            pyout(d)

    ou = line.split(' | ')[-1].split(' ')
    val = 0
    for d in ou:
        val *= 10
        srtd = "".join(sorted(d))
        val += vals[srtd]

    N += val

puzzle.answer_b = N

pyout()
