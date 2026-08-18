# 10 - Summation of primes #
def is_prime(n: int):
    if not (n & 1) or n < 2:
        return False

    return n == 2 or all(n % i for i in range(3, int(n ** 0.5) + 1, 2))


print(sum([2] + [n for n in range(3, 2_000_000, 2) if is_prime(n)]))