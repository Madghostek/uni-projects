def AsVector(n, k):
    return [1 if x == n else 0 for x in range(k)]


print(AsVector(9, 10))
