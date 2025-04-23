import os
import circle, square

def main():
    try:

        radius = float(os.getenv('RADIUS', '1.0'))
        side_length = float(os.getenv('SIDE_LENGTH', '1.0'))

        if radius < 0:
            raise ValueError("Радиус не может быть отрицательным")
        if side_length < 0:
            raise ValueError("Длина стороны квадрата не может быть отрицательной")

        circle_area = circle.area(radius)
        square_perimeter = square.perimeter(side_length)

        print(f"Площадь круга с радиусом {radius} равна {circle_area:.2f}")
        print(f"Периметр квадрата со стороной {side_length} равен {square_perimeter:.2f}")

    except ValueError as e:
        print(f"Ошибка: {e}. Пожалуйста, задайте корректные числовые значения для RADIUS и SIDE_LENGTH.")

if __name__ == "__main__":
    main()