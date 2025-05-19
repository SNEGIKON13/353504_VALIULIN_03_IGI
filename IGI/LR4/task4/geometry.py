# Module for abstract geometric figures (Task 4)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

from abc import ABC, abstractmethod
from color import FigureColor

class GeometricFigure(ABC):
    """
    Abstract base class for geometric figures.
    Declares interface for area calculation and holds color.
    """

    def __init__(self, color):
        """
        Initialize the figure with a color.
        """
        # Set and validate color via FigureColor
        self.color_obj = FigureColor(color)

    @abstractmethod
    def area(self):
        """
        Compute and return the area of the figure.
        """
        pass