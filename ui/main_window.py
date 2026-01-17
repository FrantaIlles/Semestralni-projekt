from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QTextEdit
)
from PyQt5.QtGui import QPixmap
from api.google_books import GoogleBooksAPI
from models import book
from models.storage import Storage
from recommender.recommender import Recommender
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import requests
#import api.google_books
#print("GOOGLE BOOKS FILE:", api.google_books.__file__)


class ReadBooksWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Přečtené knihy")
        self.resize(400, 600)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.btn_delete = QPushButton("Smazat vybranou knihu")
        self.btn_delete.clicked.connect(self.delete_selected)
        layout.addWidget(self.btn_delete)

        self.btn_back = QPushButton("Zpět")
        self.btn_back.clicked.connect(self.back)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

        self.load_books()

    def load_books(self):
        self.list_widget.clear()
        books = Storage.load_read_books()

        for book in books:
            item = QListWidgetItem(f"{book.title} – {', '.join(book.authors)}")
            item.setData(Qt.UserRole, book.id)
            self.list_widget.addItem(item)

    def delete_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        book_id = item.data(Qt.UserRole)
        Storage.delete_read_book(book_id)
        self.load_books()

    def back(self):
        self.close()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Doporučovač Knih")
        self.resize(400, 600)

        layout = QVBoxLayout()

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Zadejte nazev např. 'Kokotopia'")
        layout.addWidget(self.input_title)

        self.input_category = QLineEdit()
        self.input_category.setPlaceholderText("Zadejte kategorii např. 'Science Fiction'")
        layout.addWidget(self.input_category)

        self.input_author = QLineEdit()
        self.input_author.setPlaceholderText("Zadejte autora (volitelné)")
        layout.addWidget(self.input_author)

        self.input_pages = QLineEdit()
        self.input_pages.setPlaceholderText("Minimální počet stran (volitelné)")
        layout.addWidget(self.input_pages)

        self.btn_params = QPushButton("Doporučit podle parametrů")
        self.btn_params.clicked.connect(self.recommend_by_params)
        layout.addWidget(self.btn_params)

        self.btn_read = QPushButton("Doporučit podle přečtených knih")
        self.btn_read.clicked.connect(self.recommend_by_read)
        layout.addWidget(self.btn_read)

        # Seznam doporučených knih
        self.book_list = QListWidget()
        self.book_list.itemClicked.connect(self.on_book_selected)
        layout.addWidget(self.book_list)

        self.btn_add_read = QPushButton("Přidat do přečtených")
        self.btn_add_read.clicked.connect(self.add_to_read)
        layout.addWidget(self.btn_add_read)

        self.btn_open_read = QPushButton("Zobrazit přečtené knihy")
        self.btn_open_read.clicked.connect(self.open_read_books)
        layout.addWidget(self.btn_open_read)

        # Detail vybrané knihy
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setMaximumHeight(150)
        layout.addWidget(self.result)

        self.cover = QLabel()
        layout.addWidget(self.cover)

        self.setLayout(layout)
        
        self.current_book = None
        self.recommended_books = []

    def open_read_books(self):
        self.read_books_window = ReadBooksWindow(self)
        self.read_books_window.show()


    def show_book(self, book):
        if not book:
            self.result.setText("Nebyla nalezena žádná kniha.")
            return

        self.current_book = book
        self.result.setText(
            f"Název: {book.title}\n"
            f"Autor: {', '.join(book.authors)}\n"
            f"Kategorie: {', '.join(book.categories)}"
        )


    def show_books(self, books):
        self.book_list.clear()
        self.recommended_books = books
        
        if not books:
            self.result.setText("Nebyly nalezeny žádné knihy.")
            return
        
        for book in books:
            authors = ', '.join(book.authors) if book.authors else "Neznámý autor"
            item = QListWidgetItem(f"{book.title} – {authors}")
            item.setData(Qt.UserRole, book)
            self.book_list.addItem(item)
        
        self.result.setText(f"Nalezeno {len(books)} knih. Vyberte jednu ze seznamu.")

    def on_book_selected(self, item):
        book = item.data(Qt.UserRole)
        self.current_book = book
        
        authors = ', '.join(book.authors) if book.authors else "Neznámý"
        categories = ', '.join(book.categories) if book.categories else "Neznámá"
        description = book.description[:300] + "..." if book.description and len(book.description) > 300 else (book.description or "Bez popisu")
        
        self.result.setText(
            f"<b>Název:</b> {book.title}<br>"
            f"<b>Autor:</b> {authors}<br>"
            f"<b>Kategorie:</b> {categories}<br>"
            f"<b>Počet stran:</b> {book.pageCount or 'N/A'}<br><br>"
            f"<b>Popis:</b> {description}"
        )

    def recommend_by_params(self):
        title = self.input_title.text()
        category = self.input_category.text()
        author = self.input_author.text()
        pages = self.input_pages.text()
        pages = int(pages) if pages.isdigit() else None

        query_parts = []
        if title:
            query_parts.append(f"title:{title}")
        if category:
            query_parts.append(f"subject:{category}")
        if author:
            query_parts.append(f"inauthor:{author}")
        
        query = "+".join(query_parts) if query_parts else "book"
        
        books = GoogleBooksAPI.search(query)
        recommended = Recommender.recommend_from_params(books, title, category, author, pages, count=5)

        self.show_books(recommended)

    def recommend_by_read(self):
        read_books = Storage.load_read_books()

        if not read_books:
            self.result.setText("Nemáte uložené žádné přečtené knihy.")
            return
        
        last_book = read_books[-1]
        if last_book.authors:
            query = f"inauthor:{last_book.authors[0]}"
        elif last_book.categories:
            query = f"subject:{last_book.categories[0]}"
        else:
            query = "book"
            
        candidates = GoogleBooksAPI.search(query)

        recommended = Recommender.recommend_from_read(read_books, candidates, count=5)
        self.show_books(recommended)

    def add_to_read(self):
        if not self.current_book:
            self.result.setText("Nejprve si nech doporučit knihu.")
            return

        Storage.save_read_book(self.current_book)
        self.result.setText("Kniha byla přidána do přečtených.")



    def test_api_connection(self):
        if GoogleBooksAPI.test_connection():
            self.result.setText("✅ Spojení s Google Books API je funkční.")
        else:
            QMessageBox.critical(
                self,
                "Chyba připojení",
                "Nelze se připojit ke Google Books API.\n"
                "Zkontrolujte připojení k internetu."
            )

