from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    
    # Читаем файл как сырой текст, игнорируя любые ошибки кодировки
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Убираем невидимую метку BOM, если она есть
            content = content.lstrip('\ufeff')
            parser.read_string(content)
    except FileNotFoundError:
        raise Exception(f"Файл {filename} не найден!")

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Секция {section} не найдена в {filename}')

    return config

if __name__ == '__main__':
    print(load_config())