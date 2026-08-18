# 6 - Sum square difference #
sum_of_squares = sum(map(lambda x: x ** 2, range(1, 101)))
square_of_sum = sum(range(1, 101)) ** 2
print(square_of_sum - sum_of_squares)