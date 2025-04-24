# Module for mathematical function calculations (Task 1)
# Lab Work #3
# Developer: Valiulin Konstantin
# Date: 24.04.2025

import math

def calculate_ln_series(x, eps):
    """
    Calculate ln(1 + x) using series expansion with precision eps.
    Args:
        x (float): Input value where -1 < x <= 1
        eps (float): Desired precision
    Returns:
        None (prints result)
    """
    if not (-1 < x <= 1):
        raise ValueError("x must be in range (-1, 1]")
    if eps <= 0:
        raise ValueError("eps must be positive")
    
    result = 0
    term = x
    n = 1
    max_iterations = 500
    
    # If first term is less than or equal to eps, stop at n=1
    if abs(term) <= eps:
        n = 1
    else:
        # Add terms until |term| <= eps or max iterations reached
        while abs(term) > eps and n <= max_iterations:
            result += term
            term = -term * x * n / (n + 1)
            n += 1
        n -= 1  # Adjust n to reflect number of terms added
    
    math_result = math.log(1 + x)
    print(f"x = {x}, F(x) = {result}, n = {n}, Math F(x) = {math_result}")