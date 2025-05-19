# Module for concrete shape classes (Task 4)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

from geometry import GeometricFigure

class Rectangle(GeometricFigure):
    """
    Rectangle with width, height, and color.
    """
    # static attribute
    shape_name = "Rectangle"

    def __init__(self, width, height, color):
        """
        Initialize Rectangle with width, height, and color.
        """
        # initialize color in the base class
        super().__init__(color)
        # dynamic attributes
        self.width = width
        self.height = height

    def area(self):
        """
        Return area of the rectangle.
        """
        return self.width * self.height

    def __str__(self):
        """
        Return formatted description: name, dimensions, color, and area.
        """
        return (
            f"{self.shape_name}: width={self.width}, height={self.height}, "
            f"color={self.color_obj.color}, area={self.area():.2f}"
        )

class IsoscelesTrapezoid(GeometricFigure):
    """
    Isosceles trapezoid with bases a, b, height h, and color.
    """
    shape_name = "IsoscelesTrapezoid"

    def __init__(self, a, b, h, color):
        """
        Initialize trapezoid with bases a and b, height h, and color.
        """
        # base constructor handles color
        super().__init__(color)
        self.a = a
        self.b = b
        self.h = h

    def area(self):
        """
        Return area: (a + b) / 2 * h.
        """
        return (self.a + self.b) * self.h / 2

    def __str__(self):
        """
        Return formatted description: name, bases, height, color, and area.
        """
        return (
            f"{self.shape_name}: base a={self.a}, base b={self.b}, "
            f"height={self.h}, color={self.color_obj.color}, area={self.area():.2f}"
        )
