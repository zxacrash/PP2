n = int(input())
b = input().split()
c = 0
for i in range (n+1):
    if i%2 == 0:
        c += 1
print (c)


# with lambda
n = int(input())
numbers = map(int, input().split())
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(len(list(even_numbers)))