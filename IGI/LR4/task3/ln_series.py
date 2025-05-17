# Module for ln_series calculations (Task 3)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 17.05.2025

import math
from stats import StatsMixin

class LnSeriesCalculator(StatsMixin):
    """Calculator for ln(1+x) using Taylor series."""
    def __init__(self, eps):
        self.eps = eps
        self.x_values = []
        self.f_values = []
        self.n_values = []
        self.math_f_values = []

    @property
    def eps(self):
        """Precision of series; must be positive."""
        return self._eps

    @eps.setter
    def eps(self, value):
        if value <= 0:
            raise ValueError("Epsilon must be positive")
        self._eps = value

    def calculate_series(self, x):
        """
        Compute series approximation ln(1+x).

        x: argument, -1 < x <= 1.
        returns (series value, number of terms used).
        """
        if not (-1 < x <= 1):
            raise ValueError("x must be in range (-1,1]")
        result = 0.0
        term = x
        n = 1
        while abs(term) > self.eps:
            result += term
            term = -term * x * n / (n + 1)
            n += 1
        return result, n

    @staticmethod
    def calculate_math( x):
        """Compute ln(1+x) via math.log."""
        return math.log(1 + x)

    def compute_sequence(self, x_start, x_end, step):
        """Populate sequences for plotting and statistics."""
        if x_start <= -1 or x_end > 1 or step <= 0 or x_start >= x_end:
            raise ValueError("Invalid range or step")
        x = x_start
        while x <= x_end + step / 2:
            f_val, n_val = self.calculate_series(x)
            math_val = self.calculate_math(x)
            self.x_values.append(x)
            self.f_values.append(f_val)
            self.n_values.append(n_val)
            self.math_f_values.append(math_val)
            x = round(x + step, 10)