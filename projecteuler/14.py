# 14 - Longest Collatz sequence #
import time


def memoize(f):
    cache = {}

    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = f(*args, **kwargs)

        return cache[key]

    return wrapper


@memoize
def collatz_len(n: int) -> int:
    if n > 1:
        return 1 + collatz_len(3 * n + 1 if n & 1 else n // 2)

    return 0


start = time.time()
print(max({n: collatz_len(n) for n in range(1_000_000)}.items(), key=lambda e: e[1]))
end = time.time()
print(f"took {end - start:.5f} seconds")