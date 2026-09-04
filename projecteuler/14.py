# 14 - Longest Collatz sequence #
import time

from projecteuler.utils import cache


@cache
def collatz_len(n: int) -> int:
    if n > 1:
        return 1 + collatz_len(3 * n + 1 if n & 1 else n // 2)

    return 0


start = time.time()
print(max({n: collatz_len(n) for n in range(1_000_000)}.items(), key=lambda e: e[1]))
end = time.time()
print(f"took {end - start:.5f} seconds")