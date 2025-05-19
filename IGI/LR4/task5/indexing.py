# Module for NumPy indexing and slicing utilities (Task 5)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

def get_element(matrix, i, j):
    """
    Return element at position (i, j).
    """
    return matrix[i, j]


def get_row(matrix, i):
    """
    Return the i-th row as a 1D array (slice by row index).
    """
    return matrix[i, :]


def get_column(matrix, j):
    """
    Return the j-th column as a 1D array.
    """
    return matrix[:, j]


def get_submatrix(matrix, row_slice, col_slice):
    """
    Return a submatrix using slicing objects for rows and columns.

    Args:
        row_slice (slice): slice object for rows.
        col_slice (slice): slice object for columns.
    """
    return matrix[row_slice, col_slice]


def split_even_odd_index_elements(matrix):
    """
    Extract elements at even and odd index positions (flattened index).

    Returns:
        (even_elements, odd_elements)
    """
    flat = matrix.flatten()
    even = flat[::2]
    odd = flat[1::2]
    return even, odd
