"""
This module contains the Board class and methods
"""

import copy as c


class Board:
    def __init__(self, data):
        self.data = list(map(int, data[0:3]))
