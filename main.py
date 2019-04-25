from sys import argv
import board
from collections import defaultdict


assert len(argv) > 1
assert len(argv) == 5 or len(argv) == 6
assert all(i.isdigit() for i in argv[1:4] + argv[5:])
assert argv[4] in ["p", "q"]

# Subtract one so we can index at 0
SP_BLOCKS = defaultdict(lambda: board.BlockTag.NORMAL, {
    int(argv[1]): board.BlockTag.GOAL,
    int(argv[2]): board.BlockTag.FORBIDDEN,
    int(argv[3]): board.BlockTag.WALL
})
B = board.Board(SP_BLOCKS, (4, 3), 0.5, 0.1)
