# lambdas = [(lambda x: x * i) for i in range(5)]
# closures = [lmbda.__closure__ for lmbda in lambdas]
# closure_values = [type(closure[0]) for closure in closures]
#
# print(*closures, sep='\n')
# print([lmbda(1) for lmbda in lambdas])



# import threading
#
# barrier = threading.Barrier(2)
# counter = 0
#
# def worker():
#     global counter
#     barrier.wait()
#     for _ in range(50):
#         counter += 1
#
# t1 = threading.Thread(target=worker)
# t2 = threading.Thread(target=worker)
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# print(f"Final counter: {counter}")


class Unproxy:
    def __ror__(self, other):
        return other
UNPROXY = Unproxy()
def unproxy(proxy):
    return proxy | UNPROXY

class Meta(type):
    def __init__(self, *args):
        super().__init__(*args)
        selfdict = unproxy(self.__dict__)
        selfdict["__call__"] = lambda *_: 42

class NotCallable(metaclass=Meta):
    pass

not_callable = NotCallable()
print(hasattr(not_callable, "__call__")) # True
print(callable(not_callable)) # False (correctly)
print(f"{not_callable.__call__() = }")
