"""
This module contains the Board and methods
"""

from dataclasses import dataclass
from enum import Enum


class BlockTag(Enum):
    """
    A value specifying specifying whether the position is either forbidden, a
    wall, or the goal
    """
    NORMAL = 0
    WALL = 1
    FORBIDDEN = 2
    GOAL = 3

@dataclass
class Block:
    """
    A square space on the board
    tag:    The BlockTag value for the state
    q_val:  The q value at that state
    """
    tag: BlockTag
    q_val: int


class Board:
    """The current state of the board, with q-values and agent position

    Attributes:
        agent_pos:  The agent's current position
        blocks:     The set of positions on the board

    """

    def __init__(self, data):
        self.data = list(map(int, data[0:3]))
        self.blocks = []

    def _populate_board(self, goal, forbbidden, wall):
        for _ in range(0, 12):
            self.blocks.append(Block(0, 0))

    def x(self):
        return 1

    def y(self):
        return 1
