import re
text = input()
pattern = r"\d{2,}"
matches = re.findall(pattern, text)
print(" ".join(matches))