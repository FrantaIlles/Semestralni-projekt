import json
from models.book import Book

class Storage:
    FILE = "read_books.json"

    @staticmethod
    def load_read_books():
        try:
            with open(Storage.FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Book(**item) for item in data]
        except FileNotFoundError:
            return []
        
    @staticmethod
    def save_read_book(book: Book):
        books = Storage.load_read_books()

        if any(b.id == book.id for b in books):
            return
        
        books.append(book)

        with open(Storage.FILE, "w", encoding="utf-8") as f:
            json.dump([b.__dict__ for b in books], f, indent=4, ensure_ascii=False)

    @staticmethod
    def delete_read_book(book_id):
        books = Storage.load_read_books()
        books = [b for b in books if b.id != book_id]

        with open(Storage.FILE, "w", encoding="utf-8") as f:
            json.dump([b.__dict__ for b in books], f, indent=2, ensure_ascii=False)
            