def reverse_generator(s):
    a = len(s) - 1
    for i in range(a, -1, -1):
        yield s[i]
try:
    s = input()
    for char in reverse_generator(s):
        print(char, end="")