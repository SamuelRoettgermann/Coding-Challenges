class Composition:
    def __init__(self, f):
        self.f = f

    def __rshift__(self, g):
        def wrapper(*args):
            return g(self.f(*args))

        return Composition(wrapper)

    def __call__(self, *args):
        return self.f(*args)


@Composition
def compose(*args):
    return args[0] if len(args) == 1 else args


# example function
def flatten(*xss) -> list:
    return [
        x
        for xs in xss
        for x in (flatten(*xs) if isinstance(xs, (list, tuple, set)) else (xs,))
    ]


# example for function composition
none_recursive = compose >> flatten >> any >> (lambda x: not x)  # read as: apply flatten then any then the lambda
none_recursive_print = compose >> none_recursive >> print

# example for function composition calls
print(none_recursive([[0, False], [("",)]]))  # prints True
none_recursive_print([0, [1]])  # prints False