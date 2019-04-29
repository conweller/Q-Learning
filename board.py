"""
This module contains the Board class and methods
"""

from enum import Enum
from dataclasses import dataclass
import random
import functools


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

    Attributes:
        reward: The reward value for that block type
    """
    NORMAL = (-0.1)
    WALL = (None)
    FORBIDDEN = (-100)
    GOAL = (100)

    def __init__(self, reward):
        self.reward = reward


class Direction(Enum):
    """
    A direction an agent can move from a Block (direction exit returns an agent
        to the start state)

    Attributes:
        char: The character representation of the direction
        index: A function for getting the index of a block after moving from
            index (i, j) in the direction specified by the instance of the enum.
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
    """
    A square space on the board

    Attributes:
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
        return '<' + str(self.idx + 1) + ', ' + self.tag.name + '>'

    def __repr__(self):
        return str(self)


@functools.total_ordering
@dataclass
class Action:
    """
    An action that an agent can take from a Block

    Attributes:
        direction:      The direction the agent moves with the action
        destination:    The agent's position after taking the action
        q_val:          The q value for the action

    """
    direction: Direction
    dest: Block
    q_val: int

    def __lt__(self, other):
        """Is self's q_val less than other's?"""
        return self.q_val < other.q_val

    def __eq__(self, other):
        """True if q_val are equal"""
        return self.q_val == other.q_val


class Board:
    """
    The current state of the board, with q-values and agent position

    Attributes:
        agent_pos:  The agent's current block
        blocks:     The set of positions on the board

    """

    def __init__(self, sp_blocks):
        """
        Constructor for a board object

        Arguments:
            sp_blocks:  Dictionary containing special block (non-normal)
                indexes as keys and the corresponding BlockTag, either GOAL,
                FORBIDDEN, or WALL, as the values.

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
                    block.acts.append(Action(drn, self.start, 0))

    def step(self):
        """
        Choose the next action for the agent and update the q value for that
            action. Returns True that actions q value has not changed

        Note:
            Based on epsilon greedy method:
                With a probability of epsilon select a random adjacent block.
                With a probability of 1-epsilon select adjacent block with
                highest q_value.
        Returns:
            True if the previous q value for that action is the same as the new
                q value, else False
        """
        if random.random() < epsilon:
            action = random.choice(self.agent_pos.acts)
        else:
            action = max(act for act in self.agent_pos.acts)
        old_q = action.q_val
        qmax = max(act.q_val for act in action.dest.acts)
        action.q_val = (1-ALPHA) * action.q_val + ALPHA *\
            (self.agent_pos.reward + GAMMA * qmax)
        self.agent_pos = action.dest
        return old_q == action.q_val

    def next(self):
        """
        Complete one iteration of q-learning on the board, i.e. goes from the
            start state to an exit state, returns True if all q-values have
            converged

        Returns:
            True if all q-values have converged, else false
        """
        converged = True
        while self.agent_pos.tag == BlockTag.NORMAL:
            converged = self.step() and converged
        converged = self.step() and converged
        return converged

    def run(self, num_iter):
        """
        Runs a maximum num_iter iterations of q_learning. Checks for two-digit
            precision and sets epsilon to 0 when convergence is reached

        Arguments:
            num_iter:   The number of iterations to run
        """
        for _ in range(0, num_iter):
            global epsilon
            if self.next():
                epsilon = 0
