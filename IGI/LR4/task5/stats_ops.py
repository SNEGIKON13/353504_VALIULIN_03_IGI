# Module for mathematical and statistical operations with NumPy (Task 5)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

import numpy as np


def row_sums(matrix):
    """
    Compute sum of elements for each row.
    """
    return np.sum(matrix, axis=1)


def min_row_sum(matrix):
    """
    Find the minimum among all row sums.
    """
    sums = row_sums(matrix)
    return np.min(sums)


def compute_mean(matrix):
    """
    Compute the mean of all elements.
    """
    return np.mean(matrix)


def compute_median(matrix):
    """
    Compute the median of all elements.
    """
    return np.median(matrix)


def compute_variance(matrix):
    """
    Compute the variance of all elements.
    """
    return np.var(matrix)


def compute_std(matrix):
    """
    Compute the standard deviation of all elements.
    """
    return np.std(matrix)


def compute_corrcoef(even, odd):
    """
    Compute Pearson correlation coefficient between two sequences of equal length.
    If lengths differ, truncate to the smaller length.

    Args:
        even (array-like): Values at even indices.
        odd (array-like): Values at odd indices.

    Returns:
        float: correlation coefficient (scalar)
    """
    # Ensure same length by truncating to the shorter sequence
    min_len = min(len(even), len(odd))
    ev = np.asarray(even)[:min_len]
    od = np.asarray(odd)[:min_len]
    if min_len < 2:
        raise ValueError("Not enough data points to compute correlation")
    corr_matrix = np.corrcoef(ev, od)
    # corr_matrix is 2x2; element [0,1] is the correlation coefficient
    return corr_matrix[0, 1]
