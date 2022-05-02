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

        self.memory = 100  # Sets how far back the grid memorizes the position
        self.periodicity = (
            np.inf
        )  # This sets how repetitive the current state is. If = 0 it is still

        # These are the last n arrays (used to find periodic patterns)
        self.lastarrays = [self.array]

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
        grid.array = array
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

    def randomize2(self, sparseness=2):
        """
        Initializes with random start values
        """
        self.array = (
            np.logical_not(
                np.random.randint(0, high=sparseness + 1, size=(self.height, self.width))
            ).astype(bool)
        ).astype(int)

    def randomize(self, sparseness=2, width=5, height=5):
        """
        Initializes with random start values
        """
        middlearray = (
            np.logical_not(np.random.randint(0, high=sparseness + 1, size=(height, width))).astype(
                bool
            )
        ).astype(int)
        self.array = np.zeros((self.height, self.width), dtype=int)
        startx = int(self.height / 2 - height / 2)
        starty = int(self.width / 2 - width / 2)
        self.array[startx : startx + height, starty : starty + height] = middlearray

    def step(self, set_self=True, check_periodicity=True):
        """
        Applies the rule once

        Args:
         - set_self (bool) : If to update itself
        """
        self.calc_neighbours_alternative()

        if set_self:
            if check_periodicity:
                self.lastarrays[-1] = self.array
                self.array = self.apply_rule()
                self.lastarrays.append(self.array)
                self.limit_lastarrays()
                self.check_periodicity()
            else:
                # Just do it quicker
                self.array = self.apply_rule()

            return self.array
        else:
            array = self.apply_rule()
            return array

    def reset_lastarrays():
        """
        Resets the lastarray to the current state
        """

    def limit_lastarrays(self):
        """
        Limits lastarrays to a given size, set by self.memory
        """
        if len(self.lastarrays) > self.memory:
            self.lastarrays = self.lastarrays[-self.memory :]

    def check_periodicity(self):
        """
        Checks if lastarraylist is periodic
        """
        # inverse array first (start from the back)
        array_A = self.lastarrays[-1]

        for i, array_B in enumerate(reversed(self.lastarrays[:-1])):
            if np.all(array_A == array_B):
                # periodic!
                # print("Periodic state found! Periodicity: ", i)
                self.lastarrays = self.lastarrays[-i:]
                self.periodicity = i
                return i

    def multiple_steps(self, nsteps, set_self=True, check_periodicity=True, only_last=False):
        """
        Applies the rule multiple times

        Args:
         - set_self (bool) : If to update itself
        """

        if not only_last:
            newarray = np.zeros((nsteps, np.shape(self.array)[0], np.shape(self.array)[1]))
            for i in range(0, nsteps):
                newarray[i] = self.step(set_self=set_self, check_periodicity=check_periodicity)
            return newarray
        else:
            for i in range(0, nsteps):
                self.step(set_self=set_self, check_periodicity=check_periodicity)
            return self.array

    def apply_rule(self):
        """
        applies a rule to a certain entry
        """
        # no_states, no_neighbours = self.Rule.rule_array.shape

        # Commented out for speed reasons
        # if self.array.any() > no_states:
        #    print("Too many states for the applied rule set")
        #    return

        # if self.neighbouring_array.any() > no_neighbours:
        #    print("Too many neighbours for the applied rule set")
        #    return

        return self.Rule.rule_array[self.array, self.neighbouring_array]

    def calc_neighbours_alternative(self):
        """
        This is a little bit faster than np.roll
        """
        self.neighbouring_array *= 0
        # roll in x
        self.neighbouring_array[1:, :] += self.array[:-1, :]
        self.neighbouring_array[0, :] += self.array[-1, :]

        # roll in x
        self.neighbouring_array[:-1, :] += self.array[1:, :]
        self.neighbouring_array[-1, :] += self.array[0, :]

        # roll in y
        self.neighbouring_array[:, 1:] += self.array[:, :-1]
        self.neighbouring_array[:, 0] += self.array[:, -1]

        # roll in y
        self.neighbouring_array[:, :-1] += self.array[:, 1:]
        self.neighbouring_array[:, -1] += self.array[:, 0]

        # roll in xy
        self.neighbouring_array[1:, 1:] += self.array[:-1, :-1]
        self.neighbouring_array[0, 0] += self.array[-1, -1]
        self.neighbouring_array[1:, 0] += self.array[:-1, -1]
        self.neighbouring_array[0, 1:] += self.array[-1, :-1]

        # roll in xy
        self.neighbouring_array[1:, :-1] += self.array[:-1, 1:]
        self.neighbouring_array[0, -1] += self.array[-1, 0]
        self.neighbouring_array[1:, -1] += self.array[:-1, 0]
        self.neighbouring_array[0, :-1] += self.array[-1, 1:]

        # roll in xy
        self.neighbouring_array[:-1, 1:] += self.array[1:, :-1]
        self.neighbouring_array[-1, 0] += self.array[0, -1]
        self.neighbouring_array[-1, 1:] += self.array[0, :-1]
        self.neighbouring_array[
            :-1,
            0,
        ] += self.array[1:, -1]

        # roll in xy
        self.neighbouring_array[:-1, :-1] += self.array[1:, 1:]
        self.neighbouring_array[-1, -1] += self.array[0, 0]
        self.neighbouring_array[-1, :-1] += self.array[0, 1:]
        self.neighbouring_array[:-1, -1] += self.array[1:, 0]

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
            self.neighbouring_array = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
            )

        elif noneigh == 7:
            # Hexagonal Neighbourhood
            self.neighbouring_array = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
                + np.roll(np.roll(array, 1, axis=1), 1, axis=0)
                + np.roll(np.roll(array, -1, axis=1), -1, axis=0)
            )

        elif noneigh == 9:
            # Moore Neighbourhood (that's how this is called)

            self.neighbouring_array = (
                np.roll(array, 1, axis=0)
                + np.roll(array, -1, axis=0)
                + np.roll(array, 1, axis=1)
                + np.roll(array, -1, axis=1)
                + np.roll(array, [1, 1], axis=(1, 0))
                + np.roll(array, [-1, 1], axis=(1, 0))
                + np.roll(array, [1, -1], axis=(1, 0))
                + np.roll(array, [-1, -1], axis=(1, 0))
            )

        elif noneigh == 13:
            self.neighbouring_array = (
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
            self.neighbouring_array = (
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

        return self.neighbouring_array

    def get_PIL_Image(
        self,
    ):
        """
        Returns an PIL from the current array
        """
        import PIL
        from PIL import ImageDraw

        myphoto = (
            PIL.Image.fromarray(np.invert(self.array.astype(bool)))
            .resize((self.width * 10, self.height * 10), 0)
            .convert("P")
        )

        # This draws the grid
        step_size = 10
        # Draw some lines
        draw = ImageDraw.Draw(myphoto)
        y_start = 0
        y_end = myphoto.height

        for x in range(0, myphoto.width + step_size, step_size):
            if x == myphoto.width:
                line = ((x - 1, y_start), (x - 1, y_end))
            else:
                line = ((x, y_start), (x, y_end))
            draw.line(line, fill=128)
        x_start = 0
        x_end = myphoto.width
        for y in range(0, myphoto.height + step_size, step_size):
            if y == myphoto.height:
                line = ((x_start, y - 1), (x_end, y - 1))
            else:
                line = ((x_start, y), (x_end, y))
            draw.line(line, fill=128)
        del draw
        return myphoto
