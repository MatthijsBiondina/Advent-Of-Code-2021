from aocd.models import Puzzle
import numpy as np

from tools import pyout

puzzle = Puzzle(year=2021, day=2)
data = puzzle.input_data.split('\n')

horizontal, depth, aim = 0, 0, 0
for command in data:
    dir, val = command.split(' ')
    if dir == "forward":
        horizontal += int(val)
        depth += aim * int(val)
    elif dir == "down":
        aim += int(val)
    elif dir == "up":
        aim -= int(val)
    else:
        pyout()

    # pyout()

puzzle.answer_b = horizontal * depth


pyout()