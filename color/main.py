import sys
import os
import re

# ANSI escape codes for text coloring
COLOR_CODES = {
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
}

# Функция для чтения и парсинга шрифта
def parse_ascii_art(banner_file):
    if not os.path.exists(banner_file):
        print(f"Error: The banner file '{banner_file}' does not exist.")
        sys.exit(1)
        
    with open(banner_file, 'r') as file:
        lines = file.read().splitlines()  # Разделяем строки на символы по строкам
        
    symbols_dict = {}
    current_symbol = []
    current_symbol_code = 32  # Начинаем с ASCII кода пробела

    for line in lines:
        if len(line) == 0:  # Пустая строка - значит, это конец одного символа
            if current_symbol:
                symbols_dict[current_symbol_code] = current_symbol
                current_symbol = []
                current_symbol_code += 1
        else:
            current_symbol.append(line)
    
    # Не забываем добавить последний символ
    if current_symbol:
        symbols_dict[current_symbol_code] = current_symbol
    
    return symbols_dict

# Функция для добавления цвета в строку
def add_color_to_text(text, color, letters_to_color):
    color_code = COLOR_CODES.get(color.lower(), COLOR_CODES['reset'])  # Получаем цвет, если он есть
    reset_code = COLOR_CODES['reset']

    # Если указаны буквы, то только они окрашиваются
    if letters_to_color:
        letters_to_color = set(letters_to_color)  # Множество символов для ускоренного поиска
        colored_text = ""
        for char in text:
            if char in letters_to_color:
                colored_text += f"{color_code}{char}{reset_code}"
            else:
                colored_text += char
        return colored_text
    # Если не указаны буквы, то весь текст окрашивается
    else:
        return f"{color_code}{text}{reset_code}"

# Функция для преобразования текста в ASCII-арт
def text_to_ascii_art(text, banner_file, color=None, letters_to_color=None):
    symbols_dict = parse_ascii_art(banner_file)
    
    # Создаём пустой список строк для хранения результирующего ASCII-арта
    ascii_art_lines = ['' for _ in range(8)]  # Каждый символ в ASCII-арте занимает 8 строк
    
    # Обрабатываем каждый символ в тексте
    for char in text:
        ascii_code = ord(char)
        # Получаем ASCII-арт для символа или дефолтный пробел
        char_art = symbols_dict.get(ascii_code, symbols_dict.get(32))
        
        # Добавляем каждую строку символа в соответствующую строку итогового ASCII-арта
        for i in range(8):
            ascii_art_lines[i] += char_art[i]
    
    # Если задан цвет, то окрашиваем весь ASCII-арт
    if color:
        ascii_art_lines = [add_color_to_text(line, color, letters_to_color) for line in ascii_art_lines]

    # Выводим итоговый ASCII-арт
    for line in ascii_art_lines:
        print(line)

# Основная функция для обработки аргументов и вызова нужных функций
def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python main.py [OPTION] [STRING]")
        print("EX: python main.py --color=<color> <letters to be colored> \"something\"")
        sys.exit(1)

    # Определяем параметры
    color = None
    letters_to_color = None
    text = ""
    banner_name = "standard"  # По умолчанию используем шрифт "standard"
    
    # Обрабатываем флаг --color
    if sys.argv[1].startswith("--color="):
        match = re.match(r'--color=([a-zA-Z]+)\s*(.*)', sys.argv[1])
        if match:
            color = match.group(1)
            letters_to_color = match.group(2) if match.group(2) else None
            text = sys.argv[2]
        else:
            print("Usage: python main.py [OPTION] [STRING]")
            sys.exit(1)
    else:
        text = sys.argv[1]
    
    # Шрифт, если указан
    if len(sys.argv) == 3 and not sys.argv[1].startswith("--color="):
        banner_name = sys.argv[2]
    
    banner_file = f"{banner_name}.txt"
    
    # Преобразуем текст в ASCII-арт с цветом
    text_to_ascii_art(text, banner_file, color, letters_to_color)

# Запуск программы
if __name__ == "__main__":
    main()
