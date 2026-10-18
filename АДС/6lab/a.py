n = int(input())
s = input().strip()

vowels = "aeiou"
v = sorted(c for c in s if c in vowels)
c = sorted(c for c in s if c not in vowels)

print("".join(v + c))