# Lab Work #3: Python Basics, Data Types, Collections, Functions, and Modules
# Version: 1.0
# Developer: Valiulin Konstantin
# Date: 24.04.2025

import math_functions_task1
import sequence_operations_task2
import string_operations_task3_4
import list_operations_task5
import utils

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n=== Laboratory Work #3 Menu ===")
        print("1. Calculate ln(1 + x) using series expansion")
        print("2. Count positive numbers until 10 is entered")
        print("3. Check if a string is hexadecimal")
        print("4. Analyze a predefined text string")
        print("5. Process a list of real numbers")
        print("6. Exit")
        
        choice = utils.input_with_validation("Enter your choice (1-6): ", lambda x: x.isdigit() and 1 <= int(x) <= 6)
        choice = int(choice)
        
        if choice == 1:
            x = float(utils.input_with_validation("Enter x (-1 < x <= 1): ", lambda x: utils.is_float(x) and -1 < float(x) <= 1))
            eps = float(utils.input_with_validation("Enter precision (eps > 0): ", lambda x: utils.is_float(x) and float(x) > 0))
            math_functions_task1.calculate_ln_series(x, eps)
        elif choice == 2:
            sequence_operations_task2.count_positive_numbers()
        elif choice == 3:
            s = input("Enter a string to check if it's hexadecimal: ")
            result = string_operations_task3_4.is_hexadecimal(s)
            print(f"The string '{s}' is{' ' if result else ' not '}hexadecimal.")
        elif choice == 4:
            string_operations_task3_4.analyze_text()
        elif choice == 5:
            n = int(utils.input_with_validation("Enter list size: ", lambda x: x.isdigit() and int(x) > 0))
            init_method = utils.input_with_validation("Initialize by (1) user input or (2) generator? ", lambda x: x in ('1', '2'))
            if init_method == '1':
                lst = utils.user_input_list(n)
            else:
                lst = list(utils.generate_sequence(n))
            list_operations_task5.process_list(lst)
        elif choice == 6:
            print("Exiting program.")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")