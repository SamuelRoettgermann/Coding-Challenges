# No real purpose/meaning for this, just thought it looked fun while skimming some of my old code
def set_bit(n: int) -> int:
    return 1 << n

def set_bits(*ns) -> int:
    x: int = 0
    for n in ns:
        x |= set_bit(n)

    return x

def bits(*ns) -> str:
    print(hex(set_bits(*ns)))

bits(4)
bits(3)
bits(0, 7)
bits(2, 5)
bits(1, 6)
bits(*range(8, 16))

print("--")
bits(60)
bits(59)
bits(56, 63)
bits(58, 61)
bits(57, 62)
bits(*range(48, 56))