import re

text = input()
pattern = r"\w+"
matches = re.findall(pattern, text)
print(len(matches))