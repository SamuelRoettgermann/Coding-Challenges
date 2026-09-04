def memoize(f):
    cache = {}

    def wrapper(*args, **kwargs):
        key = f"{args}{kwargs}"
        if key not in cache:
            cache[key] = f(*args, **kwargs)

        return cache[key]

    return wrapper


def fib(n: int):
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)

# Assuming this follows immediately and you never call fib in-between
fib = memoize(fib)


print(fib(499))