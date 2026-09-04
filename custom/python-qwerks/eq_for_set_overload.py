# less a challenge, more so just a fun weekend for someone who needs to debug such a thing in an actual codebase

class Foo:
    def __init__(self):
        self.i = 0

    def __eq__(self, other):
        self.i += 1
        return "a"

    def __hash__(self):
        return hash(self.i)

    def __repr__(self):
        return f"Foo({self.i})"

p1 = Foo()
p2 = Foo()
p1 == p2  # try to comment out this line and see seemingly absurdity

print({p1, p2})