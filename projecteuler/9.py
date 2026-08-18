# 9 - Special Pythagorean triplet #
def triplet(target: int):
    for a in range(1, target // 3):
        for b in range(a + 1, target // 2):
            c = target - a - b
            if c < b:
                break

            if a ** 2 + b ** 2 == c ** 2 and a + b + c == target:
                return a, b, c

    return 0, 0, 0


x, y, z = triplet(1000)
print(f"{x} * {y} * {z} = {x * y * z}")