# Module for abstract geometric figures (Task 4)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    """
    Abstract base class for geometric figures.
    Declares the interface for area calculation.
    """

    @abstractmethod
    def area(self):
        """
        Compute and return the area of the figure.
        """
        pass
