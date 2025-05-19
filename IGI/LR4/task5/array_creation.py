# Module for NumPy array creation and manipulation (Task 5)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

import numpy as np


def create_array_from_list(lst):
    """
    Create a NumPy array from a Python list using array().

    Args:
        lst (list): Python list of numeric values.

    Returns:
        np.ndarray: NumPy array containing the same elements.
    """
    return np.array(lst)


def create_random_matrix(n, m, low=0, high=100, dtype=int):
    """
    Generate an integer matrix A[n,m] with random values in [low, high).

    Args:
        n (int): Number of rows.
        m (int): Number of columns.
        low (int): Inclusive lower bound of random values.
        high (int): Exclusive upper bound.
        dtype (type): Data type of the matrix elements.

    Returns:
        np.ndarray: Random integer matrix of shape (n, m).
    """
    return np.random.randint(low, high, size=(n, m)).astype(dtype)


def create_zero_matrix(n, m):
    """
    Create an n×m zero matrix using zeros().
    """
    return np.zeros((n, m), dtype=int)


def create_identity_matrix(n):
    """
    Create an n×n identity matrix using eye().
    """
    return np.eye(n, dtype=int)
