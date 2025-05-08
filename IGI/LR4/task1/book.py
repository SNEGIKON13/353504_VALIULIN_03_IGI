# Module for book class (Task 1)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 08.05.2025

class Book:
    def __init__(self, title, author, year):
        self._title = title
        self._author = author
        self._year = year

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 0 or value > 2025:
            raise ValueError("Year must be an integer between 0 and 2025")
        self._year = value

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"