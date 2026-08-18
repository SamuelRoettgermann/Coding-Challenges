# 4 - Largest palindrome product (of 3-digit numbers) #
def is_palindrome(n: int):
    s = str(n)
    return s == s[::-1]


xs = {f"{a}*{b}": a * b for a in range(999, 100, -1) for b in range(999, 100, -1) if is_palindrome(a * b)}
print(max(xs.items(), key=lambda e: e[1]))