# 21 - Amicable numbers #
def divisor_sum(n: int) -> int:
    divs = [1]
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            if n // i == i:
                divs.append(i)
            else:
                divs.append(i)
                divs.append(n // i)

    return sum(divs)


amicable_ns = [n for n in range(10_000) if (x := divisor_sum(n)) != n and n == divisor_sum(x)]

print(sum(amicable_ns))