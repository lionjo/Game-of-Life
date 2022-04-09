import numpy as np

from GameOfLife.Rule import Rule


class Grid:
    """
    This is the array with 1's and 0's
    """

    def __init__(self, width: int = 100, height: int = 100, ruleDEC=None, no_neigh=9) -> None:

        self.width = width
        self.height = height
        self.array = np.zeros((int(self.height), int(self.width)), dtype=int)
        self.neighbouring_array = self.array * 0

        if ruleDEC is not None:
            self.Rule = Rule.from_DEC(ruleDEC, no_neigh)
        else:
            self.Rule = Rule()

    @classmethod
    def from_array(cls, array, rule_array=None):
        """
        Inits the Grid from an array
        """
        height, width = np.shape(array)
        grid = cls(width, height)
        grid.Rule = Rule(rule_array=rule_array)
        grid.calc_neighbours()

        return grid

    def modify_array(self, array):
        """
        Updates the array with a new one (keeps the same rule, updates the width and height)
        """
        self.height, self.width = np.shape(array)
        self.array = array
        self.calc_neighbours()

    def reset_to_zero(self):
        """
        Initializes the array with zeros
        """
        self.array = np.zeros((self.height, self.width), dtype=int)

    def randomize(self, sparseness=2):
        """
        Initializes with random start values
        """
        self.array = (
            np.logical_not(
                np.random.randint(0, high=sparseness + 1, size=(self.height, self.width))
            ).astype(bool)
        ).astype(int)

    def step(self, set_self=True):
        """
        Applies the rule once

        Args:
         - set_self (bool) : If to update itself
        """
        self.calc_neighbours()

        if set_self:
            self.array = self.apply_rule()
            return self.array
        else:
            array = self.apply_rule()
            return array

    def multiple_steps(self, nsteps, set_self=True):
        """
        Applies the rule multiple times

        Args:
         - set_self (bool) : If to update itself
        """
        newarray = np.zeros((nsteps, np.shape(self.array)[0], np.shape(self.array)[1]))
        for i in range(0, nsteps):
            newarray[i] = self.step(set_self=set_self)
        return newarray

    def apply_rule(self):
        """
        applies a rule to a certain entry
        """
        no_states, no_neighbours = self.Rule.rule_array.shape

        if self.array.any() > no_states:
            print("Too many states for the applied rule set")
            return

        if self.neighbouring_array.any() > no_neighbours:
            print("Too many neighbours for the applied rule set")
            return

        return self.Rule.rule_array[self.array, self.neighbouring_array]

    def calc_neighbours(self):
        """
        Applies a given rule to an array
        Implies periodic boundary conditions

        Returns
        - result(np.array(2D)) : A 2 D numpy array with the number of alive neighbours as entries
        """
        array = self.array
        rule = self.Rule.rule_array

        states, noneigh = np.shape(rule)

        if states != 2:
            print("Rule has more states than we can handle right now. Adjust rule.")

        if noneigh == 5:
            result = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
            )

        elif noneigh == 7:
            # Hexagonal Neighbourhood
            result = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
                + np.roll(np.roll(array, 1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), -1, axis=0)
            )

        elif noneigh == 9:
            # Moore Neighbourhood
            result = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
                + np.roll(np.roll(array, 1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, 1, axis=1), -1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), -1, axis=0)
            )

        elif noneigh == 13:
            result = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
                + np.roll(np.roll(array, 1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, 1, axis=1), -1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), -1, axis=0)
                + np.roll(array, 2, axis=0)
                + np.roll(array, -2, axis=0)
                + np.roll(array, 2, axis=1)
                + np.roll(array, -2, axis=1)
            )

        elif noneigh == 25:
            result = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
                + np.roll(np.roll(array, 1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, 1, axis=1), -1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), -1, axis=0)
                + np.roll(array, 2, axis=0)
                + np.roll(array, -2, axis=0)
                + np.roll(array, 2, axis=1)
                + np.roll(array, -2, axis=1)
                + np.roll(np.roll(array, 2, axis=1), 1, axis=0)
                + np.roll(np.roll(array, -2, axis=1), 1, axis=0)
                + np.roll(np.roll(array, 2, axis=1), -1, axis=0)
                + np.roll(np.roll(array, -2, axis=1), -1, axis=0)
                + np.roll(np.roll(array, 1, axis=1), 2, axis=0)
                + np.roll(np.roll(array, -1, axis=1), 2, axis=0)
                + np.roll(np.roll(array, 1, axis=1), -2, axis=0)
                + np.roll(np.roll(array, -1, axis=1), -2, axis=0)
                + np.roll(np.roll(array, 2, axis=1), 2, axis=0)
                + np.roll(np.roll(array, -2, axis=1), 2, axis=0)
                + np.roll(np.roll(array, 2, axis=1), -2, axis=0)
                + np.roll(np.roll(array, -2, axis=1), -2, axis=0)
            )
        else:
            print("Rule has unhandable neighbours:", noneigh)

        self.neighbouring_array = result
        return result
