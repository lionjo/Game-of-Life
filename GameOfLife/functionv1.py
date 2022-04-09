# get cell grid nxm -> 5x10
import numpy as np

m = 4
n = 4
Grid = np.zeros((m, n))
Grid[0, 1] = 1
Grid[2, 1] = 1
Grid[2, 0] = 1
Grid2 = np.copy(Grid)
for i in range(1, m - 1):
    for j in range(1, n - 1):
        S = (
            Grid[i - 1, j - 1]
            + Grid[i - 1, j]
            + Grid[i - 1, j + 1]
            + Grid[i, j - 1]
            + Grid[i, j + 1]
            + Grid[i + 1, j - 1]
            + Grid[i + 1, j]
            + Grid[i + 1, j + 1]
        )
        if Grid[i, j] == 0 and S == 3:
            Grid2[i, j] = 1
        elif Grid[i, j] == 0 and S != 3:
            Grid2[i, j] = 0
        if Grid[i, j] == 1 and S < 2 or Grid[i, j] == 1 and S > 3:
            Grid2[i, j] = 0
        elif Grid[i, j] == 1 and S in range(2, 3):
            Grid2[i, j] = 1
print(S)
print(Grid)
print(Grid2)
