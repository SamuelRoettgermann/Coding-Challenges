def flatten(*xss) -> list:
    return [x for xs in xss for x in (flatten(*xs) if isinstance(xs, (list, tuple, set)) else (xs,))]


my_list: list = [[0, False], [("",)]]
print(f"{flatten(my_list) = }")

# golfed version:
# @formatter:off
f=lambda*z:[x for y in z for x in((y,),f(*y))[type(y)in(list,tuple,set)]]
# @formatter:on
