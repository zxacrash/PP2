import re
a = input()
pattern = r"\b[a-zA-Z]{3}\b"
match = re.findall(pattern, a)
print(len(match))