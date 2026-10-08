n = int(input())
numbers = map(int, input().split())
truthy_count = sum(map(bool, numbers))

print(truthy_count)