

import re
text = input()
pattern = r"^[a-zA-Z].*[0-9]$"

if re.search(pattern, text):
    print("Yes")
else:
    print("No")