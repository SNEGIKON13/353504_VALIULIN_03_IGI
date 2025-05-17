# Module for statistics (Task 3)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 17.05.2025

import math
from collections import Counter

class StatsMixin:
    """Provides statistical methods for numeric sequences."""

    @staticmethod
    def mean(data):
        """Return arithmetic mean of the list data."""
        return sum(data) / len(data)

    @staticmethod
    def median(data):
        """Return median of the list data."""
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2:
            return sorted_data[mid]
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2

    @staticmethod
    def mode(data):
        """Return mode(s) of data, or 'All unique' if no repeats."""
        rounded = [round(value, 4) for value in data]
        counts = Counter(rounded)
        max_count = max(counts.values())
        modes = [val for val, cnt in counts.items() if cnt == max_count]
        return modes if len(modes) < len(data) else "All unique"

    def variance(self, data):
        """Population variance of data."""
        m = self.mean(data)
        return sum((value - m) ** 2 for value in data) / len(data)

    def std_dev(self, data):
        """Population standard deviation of data."""
        return math.sqrt(self.variance(data))