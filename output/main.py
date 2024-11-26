import sys
import os
from functools import reduce

def parse_ascii_art(banner_file):
    if not banner_file.endswith('.txt'):
        banner_file += '.txt'
    
    if not os.path.exists(banner_file):
        print(f"Error: The banner file '{banner_file}' does not exist.")
        sys.exit(1)
    
    with open(banner_file, 'r') as file:
        lines = file.read().splitlines()
        
    symbols_dict = {}
    current_symbol = []
    current_symbol_code = 32 

    for line in lines:
        if len(line) == 0:
            if current_symbol:
                symbols_dict[current_symbol_code] = current_symbol
                current_symbol = []
                current_symbol_code += 1
        else:
            current_symbol.append(line)
    
    if current_symbol:
        symbols_dict[current_symbol_code] = current_symbol
    
    return symbols_dict

def text_to_ascii_art(text, banner_file):
    symbols_dict = parse_ascii_art(banner_file)
    
    # Создаем список строк для каждого символа ASCII-арта
    ascii_art_lines = ['' for _ in range(8)]
    
    # Итерируем по каждому символу в тексте
    for char in text:
        ascii_code = ord(char)
        # Получаем ASCII-арт для этого символа (или пробел, если символ не найден)
        char_art = symbols_dict.get(ascii_code, symbols_dict.get(32))
        
        # Добавляем каждую строку арта символа в соответствующую строку финального ASCII-арта
        for i in range(8):
            ascii_art_lines[i] += char_art[i]  # Добавляем каждую строку арта символа
    
    return ascii_art_lines

# Функция для обработки аргументов командной строки
def handle_args():
    if len(sys.argv) < 3:
        print("Usage: python main.py [OPTION] [STRING] [BANNER]")
        sys.exit(1)
    
    output_file = None
    text = ""
    banner_file = "standard.txt"  # Файл баннера по умолчанию
    
    # Разбираем аргументы командной строки
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--output="):
            output_file = arg[len("--output="):]
        elif i == len(sys.argv) - 2:  # Предпоследний аргумент — это строка
            text = arg
        elif i == len(sys.argv) - 1:  # Последний аргумент — это файл баннера
            banner_file = arg
    
    # Если не указан файл вывода, выводим сообщение об ошибке
    if not output_file:
        print("Usage: python3 main.py [OPTION] [STRING] [BANNER]")
        sys.exit(1)

    return output_file, text, banner_file

def main():
    output_file, text, banner_file = handle_args()

    ascii_art_lines = text_to_ascii_art(text, banner_file)

    with open(output_file, 'w') as file:
        for line in ascii_art_lines:
            file.write(line + '\n')

    print(f"ASCII art written to {output_file}")

if __name__ == "__main__":
    main()
