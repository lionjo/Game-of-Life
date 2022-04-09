"""
Checks different rules by chance
"""

import numpy as np

from GameOfLife.Grid import Grid


def setup_grid(ruleDEC):
    """
    Sets up a grid with a certain ruleID
    """
    grid = Grid(ruleDEC=ruleDEC)
    grid.randomize()

    grid.multiple_steps(82)

    print(np.sum(grid.array))


for i in range(1, 1024):
    setup_grid(i)
