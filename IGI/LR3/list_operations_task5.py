# Module for list operations (Task 5)
# Lab Work #3
# Developer: Valiulin Konstantin
# Date: 24.04.2025

import utils

@utils.timer_decorator
def process_list(lst):
    """
    Process a list to find max by module and sum before last positive element.
    Args:
        lst (list): List of real numbers
    Returns:
        None (prints results)
    """
    if not lst:
        print("List is empty.")
        return
    
    # Find maximum by module
    max_abs = max(lst, key=abs)
    
    # Find sum of elements before last positive element
    last_positive_index = -1
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] > 0:
            last_positive_index = i
            break
    
    sum_before_last_positive = sum(lst[:last_positive_index]) if last_positive_index > 0 else 0
    
    print(f"List: {lst}")
    print(f"Maximum by module: {max_abs}")
    print(f"Sum before last positive element: {sum_before_last_positive}")