import sys
import os
import shutil

# Функция для парсинга файла с ASCII-артом в словарь
def parse_ascii_art(banner_file):
    # Если файл не имеет расширения .txt, добавляем его
    if not banner_file.endswith('.txt'):
        banner_file += '.txt'
    
    # Проверяем, существует ли файл
    if not os.path.exists(banner_file):
        print(f"Error: The banner file '{banner_file}' does not exist.")
        sys.exit(1)
    
    with open(banner_file, 'r') as file:
        lines = file.read().splitlines()  # Читаем файл и разделяем по строкам
        
    symbols_dict = {}
    current_symbol = []
    current_symbol_code = 32  # Начинаем с ASCII кода 32 (пробел)

    for line in lines:
        if len(line) == 0:  # Пустая строка указывает на конец арта символа
            if current_symbol:
                symbols_dict[current_symbol_code] = current_symbol
                current_symbol = []
                current_symbol_code += 1
        else:
            current_symbol.append(line)
    
    # Не забываем добавить последний символ, если нет пустой строки в конце
    if current_symbol:
        symbols_dict[current_symbol_code] = current_symbol
    
    return symbols_dict

# Функция для создания ASCII-арта для данного текста
def text_to_ascii_art(text, banner_file, align_type):
    symbols_dict = parse_ascii_art(banner_file)
    
    # Получаем ширину терминала
    terminal_width = shutil.get_terminal_size().columns

    # Создаем список строк для каждого символа ASCII-арта
    ascii_art_lines = ['' for _ in range(8)]  # Каждый символ занимает 8 строк
    
    # Итерируем по каждому символу в тексте
    for char in text:
        ascii_code = ord(char)
        # Получаем ASCII-арт для этого символа (или пробел, если символ не найден)
        char_art = symbols_dict.get(ascii_code, symbols_dict.get(32))  # По умолчанию используем пробел
        
        # Добавляем каждую строку арта символа в соответствующую строку финального ASCII-арта
        for i in range(8):
            ascii_art_lines[i] += char_art[i]  # Добавляем каждую строку арта символа

    # Применяем выравнивание
    if align_type == "center":
        ascii_art_lines = [line.center(terminal_width) for line in ascii_art_lines]
    elif align_type == "left":
        ascii_art_lines = [line.ljust(terminal_width) for line in ascii_art_lines]
    elif align_type == "right":
        ascii_art_lines = [line.rjust(terminal_width) for line in ascii_art_lines]
    elif align_type == "justify":
        # Для выравнивания по ширине мы разбиваем каждую строку на части и добавляем пробелы
        ascii_art_lines = justify_text(ascii_art_lines, terminal_width)

    return ascii_art_lines

# Функция для выравнивания текста по ширине (justify)
def justify_text(ascii_art_lines, terminal_width):
    # Разбиваем строки на отдельные слова
    justified_lines = []
    for line in ascii_art_lines:
        words = line.split(" ")
        if len(words) == 1:  # Если одно слово в строке, просто добавляем его
            justified_lines.append(line)
            continue
        
        # Считаем, сколько пробелов нужно добавить между словами
        spaces_needed = terminal_width - sum(len(word) for word in words)
        spaces_between_words = len(words) - 1
        if spaces_between_words > 0:
            space_per_gap = spaces_needed // spaces_between_words
            extra_spaces = spaces_needed % spaces_between_words
        else:
            space_per_gap = 0
            extra_spaces = 0
        
        # Строим выровненную строку с дополнительными пробелами
        justified_line = words[0]
        for i in range(1, len(words)):
            gap = space_per_gap + (1 if i <= extra_spaces else 0)
            justified_line += ' ' * gap + words[i]
        
        justified_lines.append(justified_line)
    
    return justified_lines

# Функция для обработки аргументов командной строки
def handle_args():
    if len(sys.argv) < 3:
        print("Usage: python3 main.py [OPTION] [STRING] [BANNER]")
        sys.exit(1)
    
    text = ""
    banner_file = "standard.txt"  # Файл баннера по умолчанию
    align_type = "left"  # Выравнивание по умолчанию

    # Разбираем аргументы командной строки
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--align="):
            align_type = arg[len("--align="):]
        elif i == len(sys.argv) - 2:  # Предпоследний аргумент — это строка
            text = arg
        elif i == len(sys.argv) - 1:  # Последний аргумент — это файл баннера
            banner_file = arg
    
    # Если не указан текст, выводим сообщение об ошибке
    if not text:
        print("Usage: python3 main.py [OPTION] [STRING] [BANNER]")
        sys.exit(1)

    return text, banner_file, align_type

# Главная функция
def main():
    # Разбираем аргументы командной строки
    text, banner_file, align_type = handle_args()

    # Конвертируем введенный текст в ASCII-арт
    ascii_art_lines = text_to_ascii_art(text, banner_file, align_type)

    # Выводим ASCII-арт в терминал
    for line in ascii_art_lines:
        print(line)

# Запуск программы
if __name__ == "__main__":
    main()
