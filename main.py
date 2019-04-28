from sys import argv
import board
from collections import defaultdict


assert len(argv) > 1
assert len(argv) == 5 or len(argv) == 6
assert all(i.isdigit() for i in argv[1:4] + argv[5:])
assert argv[4] in ['p', 'q']
if argv[4] == 'q':
    assert len(argv) == 6 and argv[5].isdigit

# Subtract one so we can index at 0
SP_BLOCKS = defaultdict(lambda: board.BlockTag.NORMAL, {
    int(argv[1])-1: board.BlockTag.GOAL,
    int(argv[2])-1: board.BlockTag.FORBIDDEN,
    int(argv[3])-1: board.BlockTag.WALL
})
B = board.Board(SP_BLOCKS)
B.set_actions()

for _ in range(1, 100000):
    B.choose()

if argv[4] == "p":
    for row in B.blocks:
        for block in row:
            if block.tag == board.BlockTag.NORMAL:
                action = max(act for act in block.acts)
                print(block.idx+1, end=": ")
                print(action.direction.char)

if argv[4] == "q":
    for row in B.blocks:
        for block in row:
            if block.tag == board.BlockTag.NORMAL:
                action = max(act for act in block.acts)
                print(block.idx+1, end=": ")
                print(action.direction.char)
