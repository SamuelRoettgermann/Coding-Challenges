import random

q = 10**5
m = 10**9

print(f"{q} {m}")

for i in range(q):
    k = random.randint(1, 2)
    a = random.randint(1, 10**6)
    b = random.randint(1, 10**6)
    print(f"{k} {a} {b}")
