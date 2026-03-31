from datetime import datetime

# 1. Определяем главную дату (начало семестра)
# Используем формат ГГГГ-ММ-ДД
start_date_str = "2026-02-01"
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
other_dates_str = [
    "2026-02-15",
    "2026-03-01",
    "2026-05-20"
]

print(f"{start_date_str}\n")

# 3. Перебираем даты и вычисляем разницу
for date_str in other_dates_str:
    # Конвертируем строку в объект datetime
    current_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Вычитаем даты. Результатом будет объект timedelta
    diff = current_date - start_date
    
    # .days позволяет получить чистое количество дней
    print(f"{date_str} {diff.days}")