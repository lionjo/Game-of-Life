"""
Checks different rules by chance
"""

import time

from GameOfLife.Grid import Grid


def time_me(steps):
    """
    Sets up a grid with a certain ruleID
    """
    grid = Grid(ruleDEC=225)
    grid.randomize()

    time1 = time.time()
    grid.multiple_steps(steps)
    time2 = time.time()

    print("Time needed: ", (time2 - time1) * 1000.0, "ms", "for ", steps, " steps")
    return (time2 - time1) * 1000.0


times = []
for i in range(1000, 11000, 1000):
    times.append(time_me(i))
