# Main module for testing (Task 4)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 18.05.2025

from shapes import Rectangle, IsoscelesTrapezoid
from draw import draw_rectangle, draw_trapezoid
from color import FigureColor

def get_input(prompt, cast, validate, err_msg):
    """
    Universal input validator:
    - cast: function to convert raw input (e.g., int, float, str)
    - validate: predicate that returns True for acceptable values
    - err_msg: message printed on any failure
    """
    while True:
        raw = input(prompt)
        try:
            val = cast(raw)
        except Exception:
            print(err_msg)
            continue
        if not validate(val):
            print(err_msg)
            continue
        return val

def get_color_input(prompt):
    """
    Prompt user for a color name and validate via FigureColor setter.
    If ValueError is raised, informs and repeats until success.
    """
    while True:
        raw = input(prompt)
        try:
            fc = FigureColor(raw)
            return fc.color
        except ValueError as e:
            print(f"Invalid color: {e}")

def main():
    """
    Main interactive loop:
    1) choose shape
    2) input parameters with validation
    3) create shape, print it via __str__
    4) draw and fill shape, label it
    5) option to repeat
    """
    while True:
        choice = get_input(
            "Choose shape (1=Rectangle, 2=Isosceles trapezoid): ",
            int,
            lambda x: x in (1, 2),
            "Enter 1 or 2."
        )

        if choice == 1:
            width = get_input("Width: ", float, lambda x: x > 0, "Must be a positive number.")
            height = get_input("Height: ", float, lambda x: x > 0, "Must be a positive number.")
            color = get_color_input("Color name: ")
            label = get_input("Label text: ", str, lambda s: bool(s.strip()), "Label cannot be empty.")

            rect = Rectangle(width, height, color)
            print(rect)
            draw_rectangle(rect, label)

        else:
            a = get_input("Base a: ", float, lambda x: x > 0, "Must be a positive number.")
            b = get_input("Base b: ", float, lambda x: x > 0, "Must be a positive number.")
            h = get_input("Height: ", float, lambda x: x > 0, "Must be a positive number.")
            color = get_color_input("Color name: ")
            label = get_input("Label text: ", str, lambda s: bool(s.strip()), "Label cannot be empty.")

            trap = IsoscelesTrapezoid(a, b, h, color)
            print(trap)
            draw_trapezoid(trap, label)

        again = get_input(
            "Run again? (y/n): ",
            str,
            lambda s: s.strip().lower() in ('y', 'n'),
            "Enter 'y' or 'n'."
        ).strip().lower()
        if again == 'n':
            break

if __name__ == '__main__':
    main()
