# 11 - Largest product in a grid #
import math


def load_matrix(path: str):
    with open(path) as f:
        return [list(map(int, line.split())) for line in f]


M = load_matrix("euler11.txt")
assert len(M) == len(M[0])
SIZE = len(M)
max_prod = 0
for row, xs in enumerate(M):
    for col, x in enumerate(xs):
        # check towards the right (this automatically does the left check)
        if col + 4 <= SIZE:
            max_prod = max(max_prod, math.prod(M[row][col + i] for i in range(4)))

        # check downwards (this automatically does the up check)
        if row + 4 <= SIZE:
            max_prod = max(max_prod, math.prod(M[row + i][col] for i in range(4)))

        # check diagonally downwards + right (does upwards + left automatically)
        if row + 4 <= SIZE and col + 4 <= SIZE:
            max_prod = max(max_prod, math.prod(M[row + i][col + i] for i in range(4)))

        # check diagonally downwards + left (does upwards + right automatically)
        if row + 4 <= SIZE and col - 3 >= 0:
            max_prod = max(max_prod, math.prod(M[row + i][col - i] for i in range(4)))

print(max_prod)