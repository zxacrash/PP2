n = int(input())
b = input().split()
c = map(lambda x: int(x)**2, b)
print(sum(c))