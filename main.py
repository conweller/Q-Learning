# Author: Connor Onweller
"""
hw3.py: This file reads command line input, executes a q-learning algorithm on
    the Board specified by the input, and writes the results of the algorithm
    to standard out
"""

from sys import argv
import board
from collections import defaultdict


assert len(argv) > 1
assert len(argv) == 5 or len(argv) == 6
assert all(i.isdigit() for i in argv[1:4] + argv[5:])
assert len(argv[1:4]) == len(set(argv[1:4]))
assert argv[4] in ['p', 'q']
if argv[4] == 'q':
    assert len(argv) == 6

# Subtract one so we can index at 0
SP_BLOCKS = defaultdict(lambda: board.BlockTag.NORMAL, {
    int(argv[1])-1: board.BlockTag.GOAL,
    int(argv[2])-1: board.BlockTag.FORBIDDEN,
    int(argv[3])-1: board.BlockTag.WALL
})
B = board.Board(SP_BLOCKS)
B.set_actions()

B.run(10000)

if argv[4] == "p":
    for row in B.blocks:
        for block in row:
            if block.tag == board.BlockTag.NORMAL:
                action = max(act for act in block.acts)
                print(block.idx+1, end=": ")
                print(action.direction.char)

if argv[4] == "q":
    IDX = int(argv[5])-1
    for act in B.blocks[IDX // board.COL][IDX % board.COL].acts:
        print(act.direction.char, end=": ")
        print(str.format('{0:.2f}', act.q_val))
