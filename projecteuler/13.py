# 13 - Large sum #
with open("euler13.txt") as f:
    print(str(sum(map(int, f.readlines())))[:10])