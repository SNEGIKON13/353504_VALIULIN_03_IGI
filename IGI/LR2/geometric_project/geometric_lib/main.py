import circle, square

def main():
    while True:
        try:
            # Запрашиваем ввод с клавиатуры
            print("Введите радиус круга (или 'q' для выхода):")
            radius_input = input()
            if radius_input.lower() == 'q':
                print("Выход...")
                break

            print("Введите длину стороны квадрата:")
            side_length = float(input())

            # Проверяем значения
            radius = float(radius_input)
            if radius < 0:
                raise ValueError("Радиус не может быть отрицательным")
            if side_length < 0:
                raise ValueError("Длина стороны квадрата не может быть отрицательной")

            # Вычисляем
            circle_area = circle.area(radius)
            square_perimeter = square.perimeter(side_length)

            # Выводим результат
            print(f"Площадь круга с радиусом {radius} равна {circle_area:.2f}")
            print(f"Периметр квадрата со стороной {side_length} равен {square_perimeter:.2f}")
            print()  # Пустая строка для читаемости

        except ValueError as e:
            print(f"Ошибка: {e}. Пожалуйста, введите корректные числовые значения.")
            print()

if __name__ == "__main__":
    main()