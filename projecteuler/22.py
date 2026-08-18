# 22 - Names scores #
def name_score(name: str) -> int:
    return sum(map(lambda c: ord(c) - ord('A') + 1, name))


with open("euler22.txt") as f:
    names = sorted(f.readline().replace('"', '').split(','))
    score = 0
    for idx, name in enumerate(names, start=1):
        score += name_score(name) * idx

    print(score)