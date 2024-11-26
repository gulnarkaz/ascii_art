import sys
import shutil

# Function to parse the ASCII art file into a dictionary
def parse_ascii_art(banner_file):
    with open(banner_file, 'r') as file:
        lines = file.read().splitlines()  # Read and split by newlines
        
    symbols_dict = {}
    current_symbol = []
    current_symbol_code = 32  # Start at ASCII code 32 (space)

    for line in lines:
        if len(line) == 0:  # Found a blank line, indicating the end of a character's art
            if current_symbol:
                symbols_dict[current_symbol_code] = current_symbol
                current_symbol = []
                current_symbol_code += 1
        else:
            current_symbol.append(line)
    
    # Don't forget to add the last symbol if there's no trailing empty line
    if current_symbol:
        symbols_dict[current_symbol_code] = current_symbol
    
    return symbols_dict

# Function to create the ASCII art for the given text
def text_to_ascii_art(text, banner_file, align_type, terminal_width):
    symbols_dict = parse_ascii_art(banner_file)
    
    # Prepare the list of lists for each line in the ASCII art
    ascii_art_lines = ['' for _ in range(8)]  # Since each character has 8 lines
    
    # Iterate through each character in the input text
    for char in text:
        ascii_code = ord(char)
        # Get the ASCII art lines for this character (or space if character not found)
        char_art = symbols_dict.get(ascii_code, symbols_dict.get(32))  # Default to space if char not found
        
        # Add each line of this character's art to the corresponding line of the final ASCII art
        for i in range(8):
            ascii_art_lines[i] += char_art[i]  # Append each line of the character's art
    
    # Adjust the final ASCII art for alignment
    if align_type == 'left':
        pass  # Default behavior, no need to change
    elif align_type == 'center':
        # Center align each line
        for i in range(8):
            ascii_art_lines[i] = ascii_art_lines[i].center(terminal_width)
    elif align_type == 'right':
        # Right align each line
        for i in range(8):
            ascii_art_lines[i] = ascii_art_lines[i].rjust(terminal_width)
    elif align_type == 'justify':
        # Justify align each line (except the last one)
        for i in range(7):  # Justify all lines except the last one
            words = ascii_art_lines[i].split(' ')
            if len(words) > 1:
                total_chars = sum(len(word) for word in words)
                spaces_needed = terminal_width - total_chars
                space_slots = len(words) - 1
                if space_slots > 0:
                    space_per_slot = spaces_needed // space_slots
                    extra_spaces = spaces_needed % space_slots
                    justified_line = words[0]
                    for j in range(1, len(words)):
                        spaces = ' ' * (space_per_slot + (1 if j <= extra_spaces else 0))
                        justified_line += spaces + words[j]
                    ascii_art_lines[i] = justified_line
                else:
                    ascii_art_lines[i] = ascii_art_lines[i].ljust(terminal_width)
            else:
                ascii_art_lines[i] = ascii_art_lines[i].ljust(terminal_width)
        # The last line is left-aligned
        ascii_art_lines[7] = ascii_art_lines[7].ljust(terminal_width)

    # Print the final ASCII art
    for line in ascii_art_lines:
        print(line)

# Main function to run the program
def main():
    # Ensure that we have the correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [OPTION] [STRING] [BANNER]")
        print("Example: python3 main.py --align=right something standard")
        return
    
    # Parse the arguments
    align_type = 'left'  # Default alignment
    text = sys.argv[1]  # String to convert to ASCII art

    # Check if an alignment option is provided
    if '--align' in sys.argv:
        align_idx = sys.argv.index('--align')
        if align_idx + 1 < len(sys.argv):
            align_type = sys.argv[align_idx + 1]  # Get the alignment type
    
    # Handle the banner name
    banner_name = sys.argv[2] if len(sys.argv) == 3 else "standard"  # Default banner is "standard"
    
    # Build the banner file path with .txt extension
    banner_file = f"{banner_name}.txt"
    
    # Try to open the file and handle errors if the file does not exist
    try:
        with open(banner_file, 'r') as f:
            pass  # Just check if file exists
    except FileNotFoundError:
        print(f"Error: Banner file '{banner_file}' not found.")
        return
    
    # Get the terminal width
    terminal_width = shutil.get_terminal_size().columns
    
    # Convert the input text into ASCII art
    text_to_ascii_art(text, banner_file, align_type, terminal_width)

# Run the program
if __name__ == "__main__":
    main()
