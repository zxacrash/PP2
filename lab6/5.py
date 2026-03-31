
s = input().strip()
vowels = "aeiou"
if any(char in vowels for char in s.lower()):
    print("Yes")
else:
    print("No")