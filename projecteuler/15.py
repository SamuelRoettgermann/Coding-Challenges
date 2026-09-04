# 15 - Lattice paths #
from projecteuler.utils import cache


def possibilities(n: int) -> int:
    @cache
    def helper(downs: int, rights: int) -> int:
        if not downs or not rights:
            return 1

        right = helper(downs, rights - 1)
        down = helper(downs - 1, rights)
        return right + down

    return helper(n, n)


print(f"{possibilities(2) = }")
print(f"{possibilities(20) = }")