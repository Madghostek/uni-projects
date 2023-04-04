import functools
array = [1, 0, 0, 1]
lower_bound = 0
upper_bound = 4


print(functools.reduce(lambda x, y: x*2+y, array[lower_bound:upper_bound]))
