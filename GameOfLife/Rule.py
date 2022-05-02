import numpy as np


class Rule:
    """
    The rule class
    """

    def __init__(self, rule_array=None) -> None:

        if rule_array is not None:
            self.rule_array = rule_array
        else:
            self.rule_array = np.array([[0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0, 1, 1]])

    @classmethod
    def from_DEC(cls, DEC, noneigh=9):
        """
        Inits the rule from an DEC
        """
        rule = cls()
        rule.rule_array = rule.rulefromDEC(DEC, noneigh=noneigh)
        return rule

    def returnDEC(self):
        """
        Returns the a number to the current rule
        """
        string = "".join(map(str, np.transpose(np.flip(self.rule_array)).flatten()))
        # print("String: ",string)
        return int(string, 2)

    def rulefromDEC(self, number, noneigh=9):
        """
        Converts a number to a rule. Counterpart is DECfromrule
        """
        if noneigh in [5, 7, 9, 13, 25]:
            self.rule_array = np.flip(
                np.transpose(
                    np.reshape(
                        np.array(list(np.binary_repr(number, width=2 * noneigh))), (noneigh, 2)
                    )
                )
            ).astype(int)
            return self.rule_array
        else:
            print("Argument noneigh not in [5,7,9,13,25]")
            return -1
