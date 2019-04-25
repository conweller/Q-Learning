"""
This module contains the Board and methods
"""

from enum import Enum
import functools

class BlockTag(Enum):
    """
    A value specifying specifying whether the position is either forbidden, a
    wall, or the goal
    reward: the reward value for that block type
    """
    NORMAL = (-0.1)
    WALL = (None)
    FORBIDDEN = (-100)
    GOAL = (100)

    def __init__(self, reward):
        self.reward = reward


@functools.total_ordering
class Block:
    """A square space on the board
    tag:    The BlockTag value for the state
    q_val:  The q value at that state
    adj:    The list of blocks adjacent to self
    idx:    The block id, i.e. the index of the block
    """

    def __init__(self, idx, tag, q_val):
        self.tag = tag
        self.q_val = q_val
        self.adj = []
        self.idx = idx

    def __str__(self):
        return '<' + str(self.idx) + self.tag.name + ', ' + str(self.q_val) + '>'

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.q_val < other.q_val

    def __eq__(self, other):
        return self.q_val == other.q_val


class Board:
    """The current state of the board, with q-values and agent position

    Attributes:
        agent_pos:  The agent's current block
        blocks:     The set of positions on the board

    """

    def __init__(self, sp_blocks, dim, alpha, gamma):
        """Constructor for a board object

        Args:
            sp_blocks:  Dictionary containing block indexes as keys and the
                corresponding BlockTag, either GOAL, FORBIDDEN, or WALL, as the
                values.
            dim:        The dimensions of the board (col x row)
            alpha:      The learning rate
            gamma:      The discount rate

        Returns:
            Board: The Board object created by the constructor, where each
                Block in blocks has the BlockTag designated to it by sp_blocks
        """
        self.col = dim[0]
        self.row = dim[1]
        self.alpha = alpha
        self.gamma = gamma
        self.blocks = []
        for i in range(0, dim[0]*dim[1]):
            self.blocks.append(Block(i, sp_blocks[i], 0))
        self.agent_pos = self.blocks[0]

    def set_adjs(self):
        """Set each block's list of available adjacent blocks."""
        for idx, block in enumerate(self.blocks):
            can_be_adj = [
                idx - self.col,
                (idx - 1) if (idx - 1) % self.col != self.col - 1 else -1,
                (idx + 1) if (idx + 1) % self.col != 0 else -1,
                idx + self.col
            ]
            block.adj = [
                self.blocks[i] for i in can_be_adj if 0 <= i < self.col *
                self.row and self.blocks[i].tag != BlockTag.WALL
            ]

    def update_q(self):
        """Update the q-value for the block at the agent's position"""
        cur = self.agent_pos
        q_next = max(b.q_val for b in cur.adj)
        cur.q_val = (1-self.alpha)*cur.q_val + self.alpha * (cur.tag.reward +
                                                             self.gamma *
                                                             q_next)
        print(cur.q_val)

    def choose(self):
        self.agent_pos = max(b for b in self.agent_pos.adj)
