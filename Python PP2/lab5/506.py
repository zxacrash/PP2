
import re
a = input()
b = r"\S+@\S+\.\S+"
c = re.search(b, a)

if c:
    print(c.group())
else:
    print("No email")