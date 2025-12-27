from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem
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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.current_book = None
        self.read_list = QListWidget()
        self.load_read_books_to_list()

        self.setWindowTitle("Doporučovač Knih")
        self.resize(400, 600)

        layout = QVBoxLayout()

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

        self.btn_add_read = QPushButton("Přidat do přečtených")
        self.btn_add_read.clicked.connect(self.add_to_read)
        layout.addWidget(self.btn_add_read)

        self.btn_read = QPushButton("Doporučit podle přečtených knih")
        self.btn_read.clicked.connect(self.recommend_by_read)
        layout.addWidget(self.btn_read)

        layout.addWidget(QLabel("Přečtené knihy:"))
        layout.addWidget(self.read_list)

        self.btn_delete = QPushButton("Smazat vybranou knihu")
        self.btn_delete.clicked.connect(self.delete_selected_book)
        layout.addWidget(self.btn_delete)

        self.result = QLabel()
        self.result.setWordWrap(True)
        layout.addWidget(self.result)

        self.cover = QLabel()
        layout.addWidget(self.cover)

        self.setLayout(layout)

        self.test_api_connection()


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


    def recommend_by_params(self):
        category = self.input_category.text()
        author = self.input_author.text()
        pages = self.input_pages.text()
        pages = int(pages) if pages.isdigit() else None

        # Sestavení vyhledávacího dotazu
        query_parts = []
        if category:
            query_parts.append(f"subject:{category}")
        if author:
            query_parts.append(f"inauthor:{author}")
        
        query = "+".join(query_parts) if query_parts else "book"
        
        books = GoogleBooksAPI.search(query)
        book = Recommender.recommend_from_params(books, category, author, pages)

        self.show_book(book)

    def recommend_by_read(self):
        read_books = Storage.load_read_books()

        if not read_books:
            self.result.setText("Nemáte uložené žádné přečtené knihy.")
            return
        
        # Preferovat autora z poslední přečtené knihy
        last_book = read_books[-1]
        if last_book.authors:
            query = f"inauthor:{last_book.authors[0]}"
        elif last_book.categories:
            query = f"subject:{last_book.categories[0]}"
        else:
            query = "book"
            
        candidates = GoogleBooksAPI.search(query)

        book = Recommender.recommend_from_read(read_books, candidates)
        self.show_book(book)

    def add_to_read(self):
        if not self.current_book:
            self.result.setText("Nejprve si nech doporučit knihu.")
            return

        Storage.save_read_book(self.current_book)
        self.load_read_books_to_list()
        self.result.setText("Kniha byla přidána do přečtených.")

    def load_read_books_to_list(self):
        self.read_list.clear()
        books = Storage.load_read_books()

        for book in books:
            item = QListWidgetItem(f"{book.title} – {', '.join(book.authors)}")
            item.setData(Qt.UserRole, book.id) 
            self.read_list.addItem(item)

    def delete_selected_book(self):
        item = self.read_list.currentItem()

        if not item:
            self.result.setText("Vyber knihu, kterou chceš smazat.")
            return
        
        book_id = item.data(Qt.UserRole)
        Storage.delete_read_book(book_id)
        self.load_read_books_to_list()
        self.result.setText("Kniha byla smazána ze seznamu.")

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



        