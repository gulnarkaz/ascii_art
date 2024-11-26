from functools import reduce
import sys


def parse_ascii_art(banner_file):
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
    
    ascii_art_lines = ['' for _ in range(8)] 
    for char in text:
        ascii_code = ord(char)
        char_art = symbols_dict.get(ascii_code, symbols_dict.get(32)) 
        for i in range(8):
            ascii_art_lines[i] += char_art[i]  
 
    for line in ascii_art_lines:
        print(line)

def main():
    # Use 'standard.txt' as the default banner file
    banner_file = "standard.txt"
    text = input().strip() 
    text_to_ascii_art(text, banner_file)

if __name__ == "__main__":
    main()
