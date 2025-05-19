---

## layout: documentation

# Лабораторная работа №4 — Вопросы и ответы

Ниже приведён подробный обзор теоретической части по каждому вопросу с ссылками на реализацию в коде (названия модулей и функций). Алгоритм решения опущен, вместо него объясняются ключевые моменты, особенно работа регулярных выражений.

---

## 1. Методы у классов `csv` и `pickle`

**Теория:**

* **`csv`** — модуль для работы с табличными данными в формате CSV (Comma-Separated Values).

  * Основной класс-утилита: `csv.writer`/`csv.reader`.
  * `writer.writerow(iterable)` — записывает строку (список значений) в файл.
  * `reader = csv.reader(file)` — создаёт итератор по строкам файла.

* **`pickle`** — модуль для сериализации и десериализации Python-объектов.

  * `pickle.dump(obj, file)` — сериализует объект `obj` в бинарный поток `file`.
  * `pickle.load(file)` — восстанавливает объект из бинарного потока `file`.

```python
# library_catalog.py

import csv
import pickle
from book import Book

class LibraryCatalog:
    # ...

    def save_to_csv(self, filename='library.csv'):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author', 'Year'])  # header
            for book in self.books:
                writer.writerow([book.title, book.author, book.year])

    def load_from_csv(self, filename='library.csv'):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # пропустить заголовок
            for row in reader:
                self.add_book(Book(row[0], row[1], int(row[2])))

    def save_to_pickle(self, filename='library.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def load_from_pickle(self, filename='library.pkl'):
        with open(filename, 'rb') as file:
            loaded = pickle.load(file)
            self.books = loaded.books
```

---

## 2. Поиск книг (пример реализации «поиска»)

**Теория:**

* Используется list comprehension для фильтрации.
* Сравнение делается без учёта регистра via `str.lower()`.

```python
# library_catalog.py

class LibraryCatalog:
    # ...
    def find_books_by_author(self, author):
        """
        Найти книги по точному совпадению автора (нечувствительно к регистру).
        """
        return [
            book for book in self.books
            if book.author.lower() == author.lower()
        ]
```

В `main()` модуле при выборе опции `2` выводятся результаты:

```python
elif choice == '2':
    author = input("Enter author: ")
    books = catalog.find_books_by_author(author)
    for book in books:
        print(book)
```

---

## 3. Регулярные выражения — основные моменты

**Теория:**

* `re.findall(pattern, text)` возвращает **все** невложенные совпадения.
* `re.search(pattern, text)` возвращает **первое** совпадение или `None`.

Примеры из личного задания:

```python
import re

# 1) Поиск слова в начале строки
re.findall(r"^\w+", "AV fjfien fiidbd")
#  => ['AV']
#    '^' — начало строки, '\w+' — одна или более буквенно-цифровых символов

# 2) Поиск подряд двух \w-символов
re.findall(r"\w\w", "AV did idic didn")
#  => ['AV', 'di', 'di', 'ci', 'di']

# 3) Поиск email-подобного шаблона без .com
re.findall(r"@\w+", emails)
#  => ['@gmail', '@mail', '@yandex']

# 4) Поиск с доменом
re.findall(r"@\w+\.\w+", "example@gmail.com, example@mail.ru")
#  => ['@gmail.com', '@mail.ru']
```

---

## 4. Специальные метасимволы `\d`, `\D`, `\w`

* `\d` — любая цифра `[0-9]`.
* `\D` — любой **не**-цифровой символ `[^0-9]`.
* `\w` — «словообразующий» символ: буква, цифра или подчёркивание `[A-Za-z0-9_]`.

```python
r"\d+"     # одна или более цифр
r"\D{3}"   # ровно три любых не-цифровых символа
r"\w{4,}"  # четыре и более \w-символа
```

---

## 5. Якоря `\A`, `\Z`, `^`, `$`

* `^` — начало строки (в большинстве режимов).
* `$` — конец строки.
* `\A` — **начало** всего текста (всегда начало).
* `\Z` — **конец** всего текста.

```python
re.search(r"\AHello", text)  # строка должна начинаться с 'Hello'
re.search(r"world\Z", text)  # строка должна заканчиваться 'world'
```

---

## 6. Построение графика

**Теория:**

* Для отображения результатов используется `matplotlib`.
* Основной класс: `Plotter` (в модуле `plotter.py`).

```python
# plotter.py
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, x, series, analytic):
        self.x = x
        self.series = series
        self.analytic = analytic

    def plot(self):
        plt.figure()
        plt.plot(self.x, self.series, marker='o', linestyle='', label="Series Approx")
        plt.plot(self.x, self.analytic, linestyle='--', label="math.log")
        plt.title("ln(1+x): Series vs Analytic")
        plt.xlabel("x")
        plt.ylabel("F(x)")
        plt.legend()
        plt.grid(True)
        plt.show()
```

---

## 7. Параметры графика: `fill`, `bound`, `color`

* **`color`** — задаёт цвет линии/точек/заполнения (`'blue'`, `'#FF00FF'`, и т.д.).
* **`fill`** (в патчах `matplotlib.patches`) — логический флаг `fill=True`, `facecolor` задаёт цвет заливки.
* **`bounds`** (`set_xlim`, `set_ylim`) — устанавливают границы видимой области по осям.

```python
# Пример в draw_rectangle (draw.py)
from matplotlib.patches import Rectangle as MplRect

def draw_rectangle(rect, label):
    fig, ax = plt.subplots()
    patch = MplRect(
        (0, 0), rect.width, rect.height,
        facecolor=rect.color_obj.color,  # заливка (fill)
        edgecolor='black',              # цвет границы (bound)
        fill=True
    )
    ax.add_patch(patch)
    ax.set_xlim(-1, rect.width+1)      # границы по X
    ax.set_ylim(-1, rect.height+1)     # границы по Y
    plt.show()
```

---

## 8. Абстрактный класс, миксины, геттеры/сеттеры

* **Абстрактный класс** (`abc.ABC`, `@abstractmethod`) — шаблон для подклассов.

  ```python
  from abc import ABC, abstractmethod
  class GeometricFigure(ABC):
      @abstractmethod
      def area(self):
          pass
  ```

* **Миксин** — класс, дающий дополнительный функционал (например, `StatsMixin` для статистики):

  ```python
  class StatsMixin:
      @staticmethod
      def mean(data): return sum(data)/len(data)
      # другие статические методы: median, variance...
  ```

* **Геттеры и сеттеры** — через декораторы `@property` и `@<prop>.setter`:

  ```python
  class Book:
      @property
      def title(self):
          return self._title

      @title.setter
      def title(self, value):
          self._title = value
  ```

---

## 9. Статические vs динамические поля и методы

* **Динамические (instance) поля** — создаются в `__init__`, привязаны к объекту.
* **Статические (class) поля** — определяются сразу в теле класса, общие для всех экземпляров.

```python
class Rectangle(GeometricFigure):
    shape_name = "Rectangle"       # статическое поле

    def __init__(self, width, height, color):
        self.width = width          # динамическое поле
        self.height = height
```

* **Статические методы** (`@staticmethod`) — не принимают `self`.
* **Класс-методы** (`@classmethod`) — принимают `cls`, работают с классом.

```python
class Example:
    @staticmethod
    def static_method():
        print("Нет доступа к экземпляру или классу")

    @classmethod
    def class_method(cls):
        print(f"Работаем с классом {cls.__name__}")
```

---

## 10. Дополнительная задача: ZIP-архивация

**Теория:**

* Модуль `zipfile` для создания/разбора ZIP-архивов.
* Основные методы:

  * `ZipFile(архив, 'w')` — открыть для записи.
  * `.write(path)` — добавить файл.
  * `.infolist()` — получить метаданные.

```python
# archiver.py
import zipfile
from datetime import datetime

def create_archive(file_path, archive_name):
  with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(file_path)

def display_archive_info(archive_name):
  with zipfile.ZipFile(archive_name, 'r') as zf:
    for info in zf.infolist():
      mod_time = datetime(*info.date_time)
      print(info.filename, info.file_size, mod_time)
```

---

### Дополнительно

* **Вызов функции с декоратором без применения декоратора:** можно обратиться к оригиналу через `Class.method.__wrapped__(...)`, но это редкий приём.
* `*args`, `**kwargs` — передача произвольного количества позиционных и ключевых аргументов.

```python
def decorator(fn):
  def wrapper(*args, **kwargs):
    # ...
    return fn(*args, **kwargs)
  return wrapper
```

---

> Документ сформирован автоматически для удобства загрузки и изучения теории к ЛР №4.
