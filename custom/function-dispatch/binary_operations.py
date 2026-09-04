from typing import Callable

if __name__ == '__main__':
    binary_operations: dict[str, Callable] = {
        'add': lambda x, y: x + y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y,
    }

    try:
        first_num, second_num = int(input("First number: ")), int(input("Second number: "))
        operation = input("Operation: ")
        print(binary_operations[operation](first_num, second_num))
    except ValueError:
        print("Invalid input")