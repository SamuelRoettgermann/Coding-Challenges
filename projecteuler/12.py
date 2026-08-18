# 12 - Highly divisible triangular number #
import time
import math


def triangular_numbers():
    n, i = 0, 1

    while True:
        n, i = n + i, i + 1
        yield n


def divisors(n: int) -> int:
    # Extract prime factors
    factors = {}
    while not (n & 1):
        factors[2] = factors.get(2, 0) + 1
        n //= 2

    for i in range(3, int(n ** 0.5), 2):
        while not (n % i):
            factors[i] = factors.get(i, 0) + 1
            n //= i

    if n > 2:
        factors[n] = factors.get(n, 0) + 1

    # https://www.wikihow.com/Determine-the-Number-of-Divisors-of-an-Integer
    return math.prod(map(lambda x: x + 1, factors.values()))


start = time.time()
x = next(x for x in triangular_numbers() if divisors(x) > 500)
end = time.time()
print(f"For {x = } there are {divisors(x)} divisors\nTook {end - start:.5f} seconds")