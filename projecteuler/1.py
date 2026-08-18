# 1 - Multiples of 3 or 5 #
if __name__ == '__main__':
    x = sum(i for i in range(1000) if not (i % 5 and i % 3))
    print(x)