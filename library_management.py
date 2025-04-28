from typing import List, Generator
from pydantic import BaseModel
from abc import ABC, abstractmethod
import json
from functools import wraps

# Pydantic model for Book
class BookModel(BaseModel):
    title: str
    author: str
    year: int


# Abstract class for Library Items
class LibraryItem(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass


# Base class for items with __str__ method
class LibraryItemBase(LibraryItem):
    def __init__(self, book_model: BookModel):
        self._book_model = book_model

    def __str__(self) -> str:
        return f"Item: {self._book_model.title}, Author: {self._book_model.author}, Year: {self._book_model.year}"


# Book class
class Book(LibraryItemBase):
    def __str__(self) -> str:
        return f"Book: {self._book_model.title}, Author: {self._book_model.author}, Year: {self._book_model.year}"


# Journal class inheriting from Book
class Journal(LibraryItemBase):
    def __str__(self) -> str:
        return f"Journal: {self._book_model.title}, Author: {self._book_model.author}, Year: {self._book_model.year}"


# Decorator for logging
def log_event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("library.log", "a") as log_file:
            log_file.write(f"Event: {func.__name__} was called with args: {args[1:]}, kwargs: {kwargs}\n")
        return result
    return wrapper


# Decorator for checking book existence
def check_book_existence(func):
    @wraps(func)
    def wrapper(self, book: LibraryItem, *args, **kwargs):
        if book not in self._books:
            raise ValueError("The book does not exist in the library.")
        return func(self, book, *args, **kwargs)
    return wrapper


# Library class
class Library:
    def __init__(self):
        self._books: List[LibraryItem] = []

    @log_event
    def add_book(self, book: LibraryItem):
        self._books.append(book)

    @check_book_existence
    def remove_book(self, book: LibraryItem):
        self._books.remove(book)

    def __iter__(self):
        return iter(self._books)

    def get_books_by_author(self, author: str) -> Generator[LibraryItem, None, None]:
        return (book for book in self._books if book._book_model.author == author)

    def save_to_file(self, filename: str):
        with open(filename, "w") as file:
              json.dump([book._book_model.model_dump() for book in self._books], file)

    def load_from_file(self, filename: str):
        with open(filename, "r") as file:
            books_data = json.load(file)
            for book_data in books_data:
                book_model = BookModel(**book_data)
                self.add_book(Book(book_model))


# Context manager for file operations
class LibraryFileManager:
    def __init__(self, library: Library, filename: str):
        self.library = library
        self.filename = filename

    def __enter__(self):
        self.library.load_from_file(self.filename)
        return self.library

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: F841
        self.library.save_to_file(self.filename)


# Example usage
if __name__ == "__main__":
    # Create library
    library = Library()

    # Create book and journal
    book = Book(BookModel(title="1984", author="George Orwell", year=1949))
    journal = Journal(BookModel(title="Science Journal", author="John Doe", year=2023))

    # Add book and journal to library
    library.add_book(book)
    library.add_book(journal)

    # Print all books
    print("Books in library:")
    for item in library:
        print(item)

    # Print books by author
    print("\nBooks by George Orwell:")
    for item in library.get_books_by_author("George Orwell"):
        print(item)

    # Save books to file
    library.save_to_file("library.json")

    # Remove a book
    library.remove_book(book)

    # Print books after removal
    print("\nBooks in library after removal:")
    for item in library:
        print(item)

    # Load books from file
    with LibraryFileManager(library, "library.json"):
        pass

    # Print books after loading from file
    print("\nBooks in library after loading from file:")
    for item in library:
        print(item)