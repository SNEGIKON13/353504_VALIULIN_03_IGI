# Utility module for common functions
# Lab Work #3
# Developer: Valiulin Konstantin
# Date: 24.04.2025

import time

def timer_decorator(func):
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def is_int(s):
    """Check if string can be converted to an integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    """Check if string can be converted to a float."""
    try:
        float(s)
        return True
    except ValueError:
        return False

def input_with_validation(prompt, validation_func):
    """
    Get user input with validation.
    Args:
        prompt (str): Input prompt
        validation_func (callable): Function to validate input
    Returns:
        str: Validated input
    """
    while True:
        try:
            value = input(prompt)
            if validation_func(value):
                return value
            print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def user_input_list(n):
    """
    Get a list of n real numbers from user input.
    Args:
        n (int): Size of the list
    Returns:
        list: List of real numbers
    """
    lst = []
    for i in range(n):
        num = float(input_with_validation(f"Enter element {i + 1}: ", is_float))
        lst.append(num)
    return lst

def generate_sequence(n):
    """
    Generate a sequence of n real numbers using yield.
    Args:
        n (int): Number of elements
    Yields:
        float: Generated numbers (e.g., multiples of 0.5)
    """
    for i in range(n):
        yield i * 0.5  # Example: 0, 0.5, 1.0, 1.5, ...