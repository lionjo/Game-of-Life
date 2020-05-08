import numpy as np


rule_example = np.array([[0,0,1,1,1,0,0,0,0],[0,0,1,0,1,0,0,1,1]])


def apply_rule(entry,neighbours,rule):
    """
    applies a rule to a certain entry
    """
    no_states,no_neighbours = rule.shape

    if(entry.any()>no_states):
        print("Too many states for the applied rule set")
        return

    if(neighbours.any()>no_neighbours):
        print("Too many neighbours for the applied rule set")
        return

    return rule[entry,neighbours]



def calc_neighbours(array,rule):
    """
    Applies a given rule to an array
    Implies periodic boundary conditions
    """
    n1 = np.roll(array,1,axis=0)
    n2 = np.roll(array,-1,axis=0)
    n3 = np.roll(array,1,axis=0)
    n4 = np.roll(array,-1,axis=0)
    n5 = np.roll(array,1,axis=1)
    n6 = np.roll(array,-1,axis=1)
    n7 = np.roll(array,1,axis=1)
    n8 = np.roll(array,-1,axis=1)

    'This is a bit static but leave it for now'
    return n1+n2+n3+n4+n5+n6+n7+n8


def next_step(array,rule):
    """
    takes in an integer array
    """

    neighbours = calc_neighbours(array,rule)
    result = apply_rule(array,neighbours,rule)
    return result

