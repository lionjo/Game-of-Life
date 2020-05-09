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
    states, noneigh = np.shape(rule)

    if(states != 2):
        print("Rule has more states than we can handle right now. Adjust rule.")

    if(noneigh == 5):
        result = np.roll(array,1,axis=0) + np.roll(array,-1,axis=0) +\
                np.roll(array,1,axis=1) + np.roll(array,-1,axis=1)

    elif(noneigh == 9):
        result = np.roll(array,1,axis=0) + np.roll(array,-1,axis=0) +\
                 np.roll(array,1,axis=1) + np.roll(array,-1,axis=1) +\
                 np.roll(np.roll(array,1,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,1,axis=1),-1,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),-1,axis=0) 

    elif(noneigh == 13):
        result = np.roll(array,1,axis=0) + np.roll(array,-1,axis=0) +\
                 np.roll(array,1,axis=1) + np.roll(array,-1,axis=1) +\
                 np.roll(np.roll(array,1,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,1,axis=1),-1,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),-1,axis=0) + \
                 np.roll(array,2,axis=0) + np.roll(array,-2,axis=0) +\
                 np.roll(array,2,axis=1) + np.roll(array,-2,axis=1)


    elif(noneigh == 25):
        result = np.roll(array,1,axis=0) + np.roll(array,-1,axis=0) +\
                 np.roll(array,1,axis=1) + np.roll(array,-1,axis=1) +\
                 np.roll(np.roll(array,1,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,1,axis=1),-1,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),-1,axis=0) + \
                 np.roll(array,2,axis=0) + np.roll(array,-2,axis=0) +\
                 np.roll(array,2,axis=1) + np.roll(array,-2,axis=1) +\
                 np.roll(np.roll(array,2,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,-2,axis=1),1,axis=0) + \
                 np.roll(np.roll(array,2,axis=1),-1,axis=0) + \
                 np.roll(np.roll(array,-2,axis=1),-1,axis=0) + \
                 np.roll(np.roll(array,1,axis=1),2,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),2,axis=0) + \
                 np.roll(np.roll(array,1,axis=1),-2,axis=0) + \
                 np.roll(np.roll(array,-1,axis=1),-2,axis=0) + \
                 np.roll(np.roll(array,2,axis=1),2,axis=0) + \
                 np.roll(np.roll(array,-2,axis=1),2,axis=0) + \
                 np.roll(np.roll(array,2,axis=1),-2,axis=0) + \
                 np.roll(np.roll(array,-2,axis=1),-2,axis=0)
    else:
        print("Rule has unhandable neighbours:", noneigh)

    return result


def next_step(array,rule):
    """
    takes in an integer array
    """

    neighbours = calc_neighbours(array,rule)
    result = apply_rule(array,neighbours,rule)
    return result

