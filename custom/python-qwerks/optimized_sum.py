import numpy as np
import time


def custom_sum_me(arr: np.ndarray) -> float:
    return np.sum(arr[::2] * arr[-1])


def custom_sum_dino(arr) -> float:
    if not arr: return 0
    total = 0
    for ind, num in enumerate(arr):
        if ind % 2 == 0:
            total += num * arr[-1]

    return total

REPETITIONS = 100
xs = list(range(10 ** 7))
xs_numpy: np.ndarray = np.array(xs)

results: list[float] = [0] * REPETITIONS


def benchmark(func, xs: list[float] | np.array, repetitions: int) -> tuple[float, float]:
    time_total: float = 0
    for i in range(repetitions):
        start_time: float = time.time()
        results[i] = func(xs)
        end_time: float = time.time()
        time_total += end_time - start_time

    average_time: float = time_total / REPETITIONS
    return time_total, average_time


print(f"{benchmark(custom_sum_me, xs_numpy, REPETITIONS) = }")
print(f"{benchmark(custom_sum_dino, xs, REPETITIONS) = }")