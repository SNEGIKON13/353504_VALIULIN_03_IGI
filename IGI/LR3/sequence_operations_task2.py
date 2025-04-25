# Module for sequence operations (Task 2)
# Lab Work #3
# Developer: Valiulin Konstantin
# Date: 24.04.2025

import utils

def count_positive_numbers():
    """
    Count the number of positive integers entered until 10 is entered.
    Returns:
        None (prints result)
    """
    count = 0
    while True:
        num = utils.input_with_validation("Enter an integer (10 to stop): ", utils.is_int)
        num = int(num)
        if num == 10:
            break
        if num > 0:
            count += 1
    print(f"Number of positive integers entered: {count}")