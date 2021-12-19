import ast
import math
import time
from copy import copy, deepcopy
from typing import Set

import cupy as np
import torch
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout, plot, poem

R = []
for xx in range(4):
    for yy in range(4):
        for zz in range(4):
            X = np.eye(3)
            for _ in range(xx):
                X = X @ np.array([[1, 0, 0],
                                  [0, 0, -1],
                                  [0, 1, 0]])
            for _ in range(yy):
                X = X @ np.array([[0, 0, 1],
                                  [0, 1, 0],
                                  [-1, 0, 0]])
            for _ in range(zz):
                X = X @ np.array([[0, -1, 0],
                                  [1, 0, 0],
                                  [0, 0, 1]])
            A = str(X)
            if str(X) not in [str(x) for x in R]:
                R.append(X)
R = np.stack(R, axis=0).astype(int)

puzzle = Puzzle(day=19, year=2021)
data = puzzle.input_data

# data = """--- scanner 0 ---
# 404,-588,-901
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621
# 553,345,-567
# 474,580,667
# -447,-329,318
# -584,868,-557
# 544,-627,-890
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401
#
# --- scanner 1 ---
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# 95,138,22
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390
#
# --- scanner 2 ---
# 649,640,665
# 682,-795,504
# -784,533,-524
# -644,584,-595
# -588,-843,648
# -30,6,44
# -674,560,763
# 500,723,-460
# 609,671,-379
# -555,-800,653
# -675,-892,-343
# 697,-426,-610
# 578,704,681
# 493,664,-388
# -671,-858,530
# -667,343,800
# 571,-461,-707
# -138,-166,112
# -889,563,-600
# 646,-828,498
# 640,759,510
# -630,509,768
# -681,-892,-333
# 673,-379,-804
# -742,-814,-386
# 577,-820,562
#
# --- scanner 3 ---
# -589,542,597
# 605,-692,669
# -500,565,-823
# -660,373,557
# -458,-679,-417
# -488,449,543
# -626,468,-788
# 338,-750,-386
# 528,-832,-391
# 562,-778,733
# -938,-730,414
# 543,643,-506
# -524,371,-870
# 407,773,750
# -104,29,83
# 378,-903,-323
# -778,-728,485
# 426,699,580
# -438,-605,-362
# -469,-447,-387
# 509,732,623
# 647,635,-688
# -868,-804,481
# 614,-800,639
# 595,780,-596
#
# --- scanner 4 ---
# 727,592,562
# -293,-554,779
# 441,611,-461
# -714,465,-776
# -743,427,-804
# -660,-479,-426
# 832,-632,460
# 927,-485,-438
# 408,393,-506
# 466,436,-512
# 110,16,151
# -258,-428,682
# -393,719,612
# -211,-452,876
# 808,-476,-593
# -575,615,604
# -485,667,467
# -680,325,-822
# -627,-443,-432
# 872,-547,-609
# 833,512,582
# 807,604,487
# 839,-516,451
# 891,-625,532
# -652,-548,-490
# 30,-46,-14"""


data = data.split('\n\n')
data = [d.split('\n')[1:] for d in data]
data = [[xyz.split(',') for xyz in d] for d in data]
data = [np.array(x, dtype=int) for x in data]


def align(S1: np.ndarray, S2: np.ndarray):
    spos1 = S1[0].copy()
    spos2 = S2[0].copy()

    scan1 = S1[1].copy()
    scan2 = S2[1].copy()

    # ROTATE
    scan2 = (R[:, None, :] @ scan2[None, :, :, None]).squeeze(-1)

    # TRANSLATE
    diff = (scan1[None, None, :, :] - scan2[:, :, None, :])
    scan2 = scan2[:, None, None, :, :] + (scan1[None, None, :, :] - scan2[:, :, None, :])[..., None, :]

    # COMPARE
    overl = (scan1[None, None, None, :, None, :] == scan2[:, :, :, None, :, :])
    overl = np.all(overl, axis=-1)
    overl = np.sum(overl, axis=(-1, -2))
    overl = np.argwhere(overl >= 12)

    if len(overl) > 0:
        ii = overl[0]
        diff = diff[ii[0], ii[1], ii[2]]
        scan2 = scan2[ii[0], ii[1], ii[2]]

        return True, (diff, scan2)
    else:
        return False, None


try:
    with open("res/day_19_scanners.txt", "r") as f:
        scanners = ast.literal_eval(f.read())

    scanners = np.array(list(scanners))
    dmatrix = scanners[None, :, :] - scanners[:, None, :]
    dmatrix = np.abs(dmatrix)
    dmatrix = np.sum(dmatrix, axis=-1)

    puzzle.answer_b = np.max(dmatrix)
except FileNotFoundError:
    data = [(np.array([0, 0, 0]), x) for x in data]

    fixed_done = []
    fixed_todo = [data[0]]
    unknown = data[1:]

    pbar = tqdm(total=len(data), desc=poem("Aligning Sensor Data"), leave=False)

    while len(fixed_todo) > 0:
        S1 = fixed_todo.pop(0)
        for ii in range(len(unknown) - 1, -1, -1):
            S2 = unknown[ii]
            overlap, realigned = align(S1, S2)
            if overlap:
                del unknown[ii]
                fixed_todo.append(realigned)

        fixed_done.append(S1)

        # scanners = [x[0] for x in fixed_done] + [x[0] for x in fixed_todo]

        pbar.update(1)

    scanners = []
    beacons: Set = set()
    for scanner in fixed_done:
        scanners.append(list(scanner[0]))
        for ii in range(scanner[1].shape[0]):
            beacons.add(tuple(scanner[1][ii].tolist()))

    # with open("res/day_19_scanners.txt", 'w+') as f:
    #     f.write(str(scanners))
    #
    # with open("res/day_19_scanners.txt", "r") as f:
    #     scanners = ast.literal_eval(f.read())

    scanners = np.array(list(scanners))
    dmatrix = scanners[None, :, :] - scanners[:, None, :]
    dmatrix = np.abs(dmatrix)
    dmatrix = np.sum(dmatrix, axis=-1)

    size = np.max(dmatrix)

    # puzzle.answer_b = np.max(dmatrix)
    # pyout(np.max(dmatrix))

    # pyout()
