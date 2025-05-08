# Module for library catalog class (Task 1)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 08.05.2025

import csv
import pickle
from book import Book  # Импорт класса Book

class LibraryCatalog:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def find_books_by_author(self, author):
        return [book for book in self.books if book.author.lower() == author.lower()]

    def sort_books_by_year(self):
        self.books.sort(key=lambda book: book.year)

    def save_to_csv(self, filename='library.csv'):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author', 'Year'])
            for book in self.books:
                writer.writerow([book.title, book.author, book.year])

    def load_from_csv(self, filename='library.csv'):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) == 3:
                        self.add_book(Book(row[0], row[1], int(row[2])))
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError:
            print("Invalid data in CSV file.")

    def save_to_pickle(self, filename='library.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    def load_from_pickle(self, filename='library.pkl'):
        try:
            with open(filename, 'rb') as file:
                loaded_catalog = pickle.load(file)
                self.books = loaded_catalog.books
        except FileNotFoundError:
            print(f"File {filename} not found.")