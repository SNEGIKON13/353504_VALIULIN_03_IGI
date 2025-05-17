# Main module for testing (Task 1)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 08.05.2025

from book import Book
from library_catalog import LibraryCatalog

def main():
    catalog = LibraryCatalog()
    while True:
        print("\n1. Add book\n2. Find books by author\n3. Sort books by year\n4. Save to CSV\n5. Load from CSV\n6. Save to pickle\n7. Load from pickle\n8. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            while True:
                try:
                    year = int(input("Enter year: "))
                    book = Book(title, author, year)
                    catalog.add_book(book)
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a valid year.")
        elif choice == '2':
            author = input("Enter author: ")
            books = catalog.find_books_by_author(author)
            if books:
                for book in books:
                    print(book)
            else:
                print("No books found.")
        elif choice == '3':
            catalog.sort_books_by_year()
            print("Books sorted by year:")
            for book in catalog.books:
                print(book)
        elif choice == '4':
            catalog.save_to_csv()
            print("Saved to CSV.")
        elif choice == '5':
            catalog.load_from_csv()
            print("Loaded from CSV.")
        elif choice == '6':
            catalog.save_to_pickle()
            print("Saved to pickle.")
        elif choice == '7':
            catalog.load_from_pickle()
            print("Loaded from pickle.")
        elif choice == '8':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()