# 7 - 10001st prime #
import time

def is_prime(n: int):
    if not (n & 1) or n < 2:
        return False

    return n == 2 or all(n % i for i in range(3, int(n ** 0.5) + 1, 2))


start = time.time()
primes = [2]
x = 3
while len(primes) < 10_001:
    if is_prime(x):
        primes.append(x)

    x += 2

end = time.time()

print(primes[-1], f"took {end - start:.5f} seconds")