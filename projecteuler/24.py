# 24 - Lexicographic permutations #
import itertools

from projecteuler.utils import compose

gen_permutations = compose >> range >> list >> itertools.permutations >> sorted
print(gen_permutations(10)[1_000_000 - 1])