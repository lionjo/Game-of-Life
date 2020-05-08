import numpy as np


def repeated(f, n):
    def rfun(p):
        return reduce(lambda x, _: f(x), xrange(n), p)
    return rfun

def next_step(arr):

    return(np.roll(arr,1,axis=0))




testarray = np.random.randint(0,high=2, size=(40,60)).astype(bool)


