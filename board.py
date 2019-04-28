"""
This module contains the Board and methods
"""

from enum import Enum
from dataclasses import dataclass
import random
import functools

# TODO move q_val to adjacents finish this
# Set tuple act as named tuple

# Number of Columns:
COL = 4
# Number of Rows:
ROW = 3
# Learning Rate:
ALPHA = 0.1
# Discount Rate:
GAMMA = 0.5
# Epsilon-Greedy Constant:
epsilon = 0.1
# Start State Index:
START = 0


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


class Direction(Enum):
    """
    Docstring
    """
    UP = ("↑", lambda i, j: (i+1, j))
    DOWN = ("↓", lambda i, j: (i-1, j))
    LEFT = ("→", lambda i, j: (i, j+1))
    RIGHT = ("←", lambda i, j: (i, j-1))
    EXIT = ("X", None)

    def __init__(self, char, index):
        self.char = char
        self.index = index


class Block:
    """A square space on the board
    tag:    The BlockTag value for the state
    acts:   The list of Actions that can be taken from this block
    idx:    The block id, i.e. the index of the block
    reward: The reward for taking an action from this block
    """

    def __init__(self, idx, tag):
        self.tag = tag
        self.idx = idx
        self.reward = tag.reward
        self.acts = []

    def __str__(self):
        return '<' + str(self.idx +1) + ', ' + self.tag.name + '>'

    def __repr__(self):
        return str(self)


@dataclass
class Action:
    """
    Docstring here
    """
    direction: Direction
    dest: Block
    q_val: int

    def __lt__(self, other):
        """Is self's q_val less than other's"""
        return self.q_val < other.q_val

    def __eq__(self, other):
        """True if q_val are equal"""
        return self.q_val == other.cakes


class Board:
    """The current state of the board, with q-values and agent position

    Attributes:
        agent_pos:  The agent's current block
        blocks:     The set of positions on the board

    """

    def __init__(self, sp_blocks):
        """Constructor for a board object

        Args:
            sp_blocks:  Dictionary containing block indexes as keys and the
                corresponding BlockTag, either GOAL, FORBIDDEN, or WALL, as the
                values.

        Returns:
            Board: The Board object created by the constructor, where each
                Block in blocks has the BlockTag designated to it by sp_blocks
        """
        self.blocks = []
        for i in range(0, ROW):
            self.blocks.append([])
            for j in range(0, COL):
                self.blocks[i].append(Block(i*COL+j, sp_blocks[i*COL+j]))
        self.start = self.blocks[START // COL][START % COL]
        self.agent_pos = self.blocks[START // COL][START % COL]

    # def set_adjs(self):
    #     for idx, block in enumerate(self.blocks):
    #         can_be_adj = [
    #             idx - COL,
    #             (idx - 1) if (idx - 1) % COL != COL - 1 else -1,
    #             (idx + 1) if (idx + 1) % COL != 0 else -1,
    #             idx + COL
    #         ]
    #         block.adj = [
    #             self.blocks[i] for i in can_be_adj if 0 <= i < (COL * ROW) and
    #             self.blocks[i].tag != BlockTag.WALL
    #         ]
    #     for block in self.blocks:
    #         if block.tag != BlockTag.NORMAL:
    #             block.adj = [self.blocks[START]]
    #         print(block.adj)

    def set_actions(self):
        """Set each block's list of available actions."""
        for i, row in enumerate(self.blocks):
            for j, block in enumerate(row):
                for drn in (d for d in Direction if d != Direction.EXIT):
                    new_i, new_j = drn.index(i, j)
                    if 0 <= new_i < ROW and 0 <= new_j < COL:
                        new_block = self.blocks[new_i][new_j]
                        if new_block.tag != BlockTag.WALL:
                            block.acts.append(Action(drn, new_block, 0))
                if block.tag != BlockTag.NORMAL:
                    block.acts = []
                    drn = Direction.EXIT
                    block.acts.append(Action(drn, self.start,0))
                # print(str(block.idx+1) +": " + str(list(map(lambda x:x.dest.idx +1,
                                                         # block.acts))))

    def update_q(self, action):
        """Update the q-value for the block at the agent's position"""
        # for action in self.agent_pos.acts:
        # action = max(self.agent_pos.acts)
        qmax = max(act.q_val for act in action.dest.acts)
        action.q_val = (1-ALPHA) * action.q_val + ALPHA *\
        (self.agent_pos.reward + GAMMA * qmax)
        # print( str(self.agent_pos.idx + 1) + ": " + str(action.dest) + ": " + str(action.q_val))
        # print(self.agent_pos.reward)

    def choose(self):
        """Choose the next position for the agent
        Note:
            Based on epsilon greedy method:
                With a probability of epsilon select a random adjacent block.
                With a probability of 1-epsilon select adjacent block with
                highest q_value.
        """
        if random.random() < epsilon:
            action = random.choice(self.agent_pos.acts)
            # self.agent_pos = action.dest
        else:
            # print((self.agent_pos.idx+1),end=": ")
            action = max(act for act in self.agent_pos.acts)
            # print(str(action.dest.idx+1))
            # self.update_q(action)
            # print(str(action.q_val))
            # self.agent_pos = action.dest
        old_q = action.q_val
        qmax = max(act.q_val for act in action.dest.acts)
        action.q_val = (1-ALPHA) * action.q_val + ALPHA *\
        (self.agent_pos.reward + GAMMA * qmax)
        self.agent_pos = action.dest
        return old_q == action.q_val
