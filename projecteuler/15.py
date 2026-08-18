# 15 - Lattice paths #
def possibilities(n: int) -> int:
    def memoize(f):
        cache = {}

        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = f(*args, **kwargs)

            return cache[key]

        return wrapper

    @memoize
    def helper(downs: int, rights: int) -> int:
        if not downs or not rights:
            return 1

        right = helper(downs, rights - 1)
        down = helper(downs - 1, rights)
        return right + down

    return helper(n, n)


print(f"{possibilities(2) = }")
print(f"{possibilities(20) = }")