import sys

# Примерный код для обработки аргументов
def display_example(example_name):
    try:
        with open("examples.txt", "r") as file:
            content = file.read()
            examples = content.split('\n\n')  # Разделяем примеры
            example_dict = {}
            for example in examples:
                lines = example.split('\n')
                example_dict[lines[0].strip()] = '\n'.join(lines[1:]).strip()

            # Выводим нужный пример
            print(example_dict.get(example_name, "Example not found"))

    except FileNotFoundError:
        print("Examples file not found!")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        example_name = sys.argv[1]
        display_example(example_name)
    else:
        print("Usage: python3 main.py [EXAMPLE_NAME]")
