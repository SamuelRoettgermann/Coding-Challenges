# 16 - Power digit sum #
def pow_dig_sum(exponent, base=2):
    return sum(map(int, str(base ** exponent)))


print(pow_dig_sum(15))  # known case
print(pow_dig_sum(1000))  # target case