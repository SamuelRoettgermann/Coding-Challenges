def f(a, *, b, c):
    print(a, b, c)

f(1, b=2, c=3) # prints 1 2 3
f(a=1, b=2, c=3) # prints 1 2 3
f(1, 2, 3, b=4, c=5)  # errror
f(1, 2, 3)  # error
f(1, 2, c=3) # error


def g(*a, b, c):
    print(a, b, c)

g(1, b=2, c=3)  # prints '(1,) 2 3'
g(1, 2, 3, 4, 5, 6, b=7, c=8)  # prints '(1, 2, 3, 4, 5, 6) 7 8'
g(1, 2, 3, 4, 5) # error

def h(a, /, b, c):
    print(a, b, c)

h(1, b=2, c=3)  # prints '1 2 3'
h(1, 2, 3)  # prints '1 2 3'
h(a=1, b=2, c=3)  # error