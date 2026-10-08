import re
text = input()
pattern = r"[A-Z]"
matches = re.findall(pattern, text)
print(len(matches))