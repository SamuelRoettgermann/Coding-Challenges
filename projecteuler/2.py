# 2 - Even Fibonacci numbers #
from projecteuler.utils import cache


@cache
def fib(n: int):
    if n <= 2:
        return n

    return fib(n - 1) + fib(n - 2)

xs = []
i = 1
while fib(i) <= 4e6:
    if not (fib(i) & 1):
        xs.append(fib(i))

    i += 1

x = sum(xs)
print(x)