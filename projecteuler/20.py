# 20 - Factorial digit sum #
from projecteuler.utils import cache


@cache
def fac(n: int) -> int:
    if n <= 1:
        return 1

    return n * fac(n - 1)


print(sum(map(int, list(str(fac(100))))))