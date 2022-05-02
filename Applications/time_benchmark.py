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
    grid.multiple_steps(steps, check_periodicity=False, only_last=True)
    time2 = time.time()

    print("Time needed: ", (time2 - time1) * 1000.0, "ms", "for ", steps, " steps")
    return (time2 - time1) * 1000.0


def time_me_gridsize(width: int, steps=3000):
    """
    Times the Grid scaling with increasing size
    """
    grid = Grid(width=width, height=width, ruleDEC=225)
    grid.randomize()

    time1 = time.time()
    grid.multiple_steps(steps, check_periodicity=False, only_last=True)
    time2 = time.time()

    print("Time needed: ", (time2 - time1) * 1000.0, "ms", "for a size of ", width, "x", width)
    return (time2 - time1) * 1000.0


times = []
for i in range(1000, 11000, 1000):
    times.append(time_me(i))

times = []
for i in range(100, 600, 100):
    times.append(time_me_gridsize(i))
