# 25 - 1000-digit Fibonacci number #
from projecteuler.utils import cache


@cache
def fib(n: int):
    if n <= 2:
        return 1

    return fib(n - 1) + fib(n - 2)


n = 1
while len(str(fib(n))) < 1000:
    n += 1

print(n)