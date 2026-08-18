# 5 - Smallest multiple #
def divisibility(x: int, ns=range(1, 21)):
    print(f"testing {x}...")
    return not any(x % n for n in ns)


x = 20
while not divisibility(x):
    x += 20

print(x)