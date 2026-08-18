class Composition:
    def __init__(self, f):
        self.f = f

    def __rshift__(self, g):
        def wrapper(*args):
            return g(self(*args))

        return Composition(wrapper)

    def __call__(self, *args):
        return self.f(*args)


@Composition
def compose(*args):
    return args[0] if len(args) == 1 else args


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance


def flatten(*xss) -> list:
    return [x for xs in xss for x in (flatten(*xs) if isinstance(xs, (list, tuple, set)) else (xs,))]


def cache(f):
    calculated = {}

    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in calculated:
            calculated[key] = f(*args, **kwargs)

        return calculated[key]

    return wrapper
