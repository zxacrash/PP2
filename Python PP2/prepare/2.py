import json

# 1. Наш JSON-список пользователей
json_data = '''
[
    {"name": "Ivan", "email": "123@gmail.com"},
    {"name": "Serega", "email": "lol_mail"},
    {"name": "Masha", "email": "masha@yandex.ru"},
    {"name": "Dimon", "email": "wrong_email@"}
]
'''

# 2. Десериализация (превращаем строку в список словарей Python)
users = json.loads(json_data)

print("Пользователи с правильной почтой:")

# 3. Проходим циклом по каждому человеку
for user in users:
    email = user["email"]
    
    # Условие "правильности": есть @ и есть точка после неё
    if "@" in email and "." in email:
        print(f"Имя: {user['name']} | Почта: {email}")