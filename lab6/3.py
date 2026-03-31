
n = int(input())
words = input().split()
result = " ".join([f"{i}:{word}" for i, word in enumerate(words)])

print(result)