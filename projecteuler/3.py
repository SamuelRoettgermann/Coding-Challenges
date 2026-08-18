# 3 - Largest prime factor #
import math

x = 600851475143
factors = []
while not (x & 1):
    factors.append(2)
    x //= 2

for i in range(3, int(math.sqrt(x)), 2):
    while not (x % i):
        factors.append(i)
        x //= i

if x > 2:
    factors.append(x)

print(factors)
print(max(factors))