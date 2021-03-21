import numpy as np

from RuleFinder import arrsampler,rulefromDEC
import time
from Rules import next_step,evolve_array

import functools



"""
This is dedicated to juding a certain rule set. 
"""


width = 400
height = 400
sparseness = 2

noneigh = 9

def repeat (f, x,y, n) :
    for i in range(n):
        x = f(x,y)
    return x


def repeat2(f, n):
    if n == 1:
        return f
    else:
        return lambda x,y: f(repeat2(f,n-1)(x,y),y)

def mass_preserving(ruleDEC):
    """
    Tries to find rules that preserve the mass
    """

    rule = rulefromDEC(ruleDEC,noneigh)
    arr = arrsampler(width, height,sparseness)

    before = np.sum(arr)
  
    newarr = repeat2(next_step,21)(arr,rule)
    #evolve_array(arr,rule,200)
    
    after = np.sum(newarr)

    return after/before



exportarray = np.zeros((1024,2))
for i in range(1,1024):
    exportarray[i-1] = np.array([i, mass_preserving(i)])
    print(exportarray[i-1])


np.savetxt("9RulesMass.txt",exportarray,fmt="%i %2.3f")