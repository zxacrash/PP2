import json
import re

json_data = '{"Ivan": "123@gmail.com", "Serega": "lol_mail"}'
data = json.loads(json_data)

for name, email in data.items():
    if re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email):
        print(name)