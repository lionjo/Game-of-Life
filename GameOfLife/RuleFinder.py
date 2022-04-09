import numpy as np


def saverule(rules, filename):
    """
    Saves the rule to a file
    """
    ruleshape = np.shape(rules)

    np.savetxt(filename, np.reshape(rules, (ruleshape[0], ruleshape[1] * ruleshape[2])), fmt="%i")


def loadrules(filename):
    """
    Loads a rule from a txt file.
    """
    rules = np.loadtxt(filename)

    norules, leng = rules.shape

    return np.reshape(rules, (norules, 2, int(leng / 2)))


def rulefromDEC(number, noneigh):
    """
    Converts a number to a rule. Counterpart is DECfromrule
    """
    if noneigh == 5 or noneigh == 7 or noneigh == 9 or noneigh == 13 or noneigh == 25:
        return np.flip(
            np.transpose(
                np.reshape(
                    np.array(list(np.binary_repr(number - 1, width=2 * noneigh))), (noneigh, 2)
                )
            )
        ).astype(int)


def DECfromrule(rule):
    """
    Converts a rule to a number. Counterpart is rulefromDEC
    """
    string = "".join(map(str, np.transpose(np.flip(rule)).flatten()))
    # print("String: ",string)
    return int(string, 2) + 1


def rulesampler(neighbours):
    if (
        neighbours == 5
        or neighbours == 7
        or neighbours == 9
        or neighbours == 13
        or neighbours == 25
    ):
        rule = np.random.randint(0, high=2, size=(2, neighbours))
        return rule
    else:
        print("No such neighbour number:", neighbours)
        return


def rulesampler_array(neighbours, length):
    return np.array([rulesampler(np.array(neighbours)) for i in range(0, length)])


def arrsampler(width, height, sparseness):
    """
    The higher sparness, the less likely are ones there
    """
    arr = (
        np.logical_not(np.random.randint(0, high=sparseness + 1, size=(width, height))).astype(bool)
    ).astype(int)
    return arr


if __name__ == "__main__":

    print(arrsampler(10, 10, 40))

    print(rulesampler_array(5, 10).shape)

    saverule(rulesampler_array(5, 100), "ruletest.txt")

    print(loadrules("ruletest.txt"))

    print(rulefromDEC(1024, 5))
    print(DECfromrule(rulefromDEC(1008, 5)))
