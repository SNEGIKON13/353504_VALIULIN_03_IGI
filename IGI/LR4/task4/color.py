# Module for figure color handling (Task 4)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

import matplotlib.colors as mcolors

class FigureColor:
    """
    Holds and validates the color description for a figure.
    """

    def __init__(self, color):
        # immediately validate through the setter
        self.color = color

    @property
    def color(self):
        """
        Get the color string.
        """
        return self._color

    @color.setter
    def color(self, value):
        """
        Validate and set the color string.
        - must be a non-empty string
        - must be recognized by matplotlib
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Color must be a non-empty string")
        col = value.strip()
        try:
            mcolors.to_rgba(col)
        except ValueError:
            raise ValueError(f"'{col}' is not a valid Matplotlib color")
        self._color = col