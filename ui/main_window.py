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
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap, QFont
from api.google_books import GoogleBooksAPI
from api.open_library import OpenLibraryAPI
from api.combined_search import CombinedSearch
from models import book
from models.storage import Storage
from recommender.recommender import Recommender
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import requests
import os


class ReadBooksWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Přečtené knihy")
        icon_path = os.path.join(os.path.dirname(__file__), "ikona.jpg")
        self.setWindowIcon(QIcon(icon_path))

        font = QFont()
        font.setPointSize(11)
        self.setFont(font)


        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Arial", 11))
        layout.addWidget(self.list_widget)

        self.btn_delete = QPushButton("Smazat vybranou knihu")
        self.btn_delete.setMinimumHeight(40)
        self.btn_delete.setFont(QFont("Arial", 11))
        self.btn_delete.clicked.connect(self.delete_selected)
        layout.addWidget(self.btn_delete)

        self.btn_back = QPushButton("Zpět")
        self.btn_back.setMinimumHeight(40)
        self.btn_back.setFont(QFont("Arial", 11))
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
        icon_path = os.path.join(os.path.dirname(__file__), "ikona.jpg")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Doporučovač Knih")
        self.resize(600, 800)

        font = QFont()
        font.setPointSize(11)
        self.setFont(font)


        layout = QVBoxLayout()

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Zadejte nazev např. 'Harry Potter'")
        self.input_title.setMinimumHeight(35)
        self.input_title.setFont(QFont("Arial", 11))
        layout.addWidget(self.input_title)

        self.input_category = QLineEdit()
        self.input_category.setPlaceholderText("Zadejte kategorii např. 'Science Fiction'")
        self.input_category.setMinimumHeight(35)
        self.input_category.setFont(QFont("Arial", 11))
        layout.addWidget(self.input_category)

        self.input_author = QLineEdit()
        self.input_author.setPlaceholderText("Zadejte autora (volitelné)")
        self.input_author.setMinimumHeight(35)
        self.input_author.setFont(QFont("Arial", 11))
        layout.addWidget(self.input_author)

        self.input_pages = QLineEdit()
        self.input_pages.setPlaceholderText("Minimální počet stran (volitelné)")
        self.input_pages.setMinimumHeight(35)
        self.input_pages.setFont(QFont("Arial", 11))
        layout.addWidget(self.input_pages)

        self.btn_params = QPushButton("Doporučit podle parametrů")
        self.btn_params.setMinimumHeight(45)
        self.btn_params.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_params.clicked.connect(self.recommend_by_params)
        layout.addWidget(self.btn_params)

        self.btn_read = QPushButton("Doporučit podle přečtených knih")
        self.btn_read.setMinimumHeight(45)
        self.btn_read.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_read.clicked.connect(self.recommend_by_read)
        layout.addWidget(self.btn_read)

        # Seznam doporučených knih
        self.book_list = QListWidget()
        self.book_list.setFont(QFont("Arial", 11))
        self.book_list.itemClicked.connect(self.on_book_selected)
        layout.addWidget(self.book_list)

        self.btn_add_read = QPushButton("Přidat do přečtených")
        self.btn_add_read.setMinimumHeight(40)
        self.btn_add_read.setFont(QFont("Arial", 11))
        self.btn_add_read.clicked.connect(self.add_to_read)
        layout.addWidget(self.btn_add_read)

        self.btn_open_read = QPushButton("Zobrazit přečtené knihy")
        self.btn_open_read.setMinimumHeight(40)
        self.btn_open_read.setFont(QFont("Arial", 11))
        self.btn_open_read.clicked.connect(self.open_read_books)
        layout.addWidget(self.btn_open_read)

        # Detail vybrané knihy
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setMaximumHeight(200)
        self.result.setFont(QFont("Arial", 11))
        layout.addWidget(self.result)

        self.cover = QLabel()
        layout.addWidget(self.cover)

        self.setLayout(layout)
        
        self.current_book = None
        self.recommended_books = []

    def open_read_books(self):
        self.read_books_window = ReadBooksWindow()
        # Převzetí velikosti a pozice hlavního okna
        self.read_books_window.resize(self.size())
        self.read_books_window.move(self.pos())
        self.read_books_window.show()


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
        title = self.input_title.text().strip()
        category = self.input_category.text().strip()
        author = self.input_author.text().strip()
        pages = self.input_pages.text().strip()
        pages = int(pages) if pages.isdigit() else None

        if not title and not category and not author and not pages:
            self.result.setText("Zadejte alespoň jeden parametr pro vyhledávání.")
            return

        query_parts = []
        if title:
            query_parts.append(f'intitle:"{title}"')  
        if author:
            query_parts.append(f'inauthor:"{author}"') 
        if category:
            query_parts.append(f'subject:"{category}"') 

        query = " ".join(query_parts) if query_parts else "book"
        
        print(f"Vyhledávací dotaz: {query}")
        books = CombinedSearch.search(query, category=category if category else None, max_results=40)
        print(f"Nalezeno knih: {len(books)}")
        
        # Filtruj podle zadaných parametrů
        recommended = Recommender.recommend_from_params(books, min_pages=pages, count=10)
        print(f"Doporučeno knih: {len(recommended)}")
        
        self.show_books(recommended)

    def recommend_by_read(self):
        read_books = Storage.load_read_books()

        if not read_books:
            self.result.setText("Nemáte uložené žádné přečtené knihy.")
            return

        print(f"Přečtených knih: {len(read_books)}")
        for b in read_books:
            print(f"  - {b.title} (autoři: {b.authors}, kategorie: {b.categories})")

        authors = []
        categories = []
        
        for b in read_books:
            if b.authors:
                authors.extend(b.authors)
            if b.categories:
                categories.extend(b.categories)

        authors = list(set(authors))
        categories = list(set(categories))

        print(f"Autoři: {authors}")
        print(f"Kategorie: {categories}")

        all_candidates = []
        
        # Hledej podle VŠECH autorů
        if authors:
            for author in authors:
                last_name = author.split()[-1] if author else ""
                if last_name and len(last_name) > 2:
                    for search_term in [last_name, author]:
                        author_query = f'inauthor:{search_term}'
                        print(f"Hledám autora: {author_query}")
                        candidates = CombinedSearch.search(author_query, max_results=20)
                        print(f"  → Nalezeno: {len(candidates)}")
                        
                        all_candidates.extend(candidates)  # Přidej všechny
                        
                        if candidates:
                            break  # Máme výsledky, nemusíme hledat znovu
        
        # Hledej podle kategorií
        if categories:
            category_query = " OR ".join([f'subject:"{c}"' for c in categories[:2]])
            print(f"Hledám kategorie: {category_query}")
            candidates = CombinedSearch.search(category_query, max_results=30)
            print(f"  → Nalezeno: {len(candidates)}")
            all_candidates.extend(candidates)

        # Odstraň duplikáty
        seen = set()
        unique_candidates = []
        for c in all_candidates:
            if c.id not in seen:
                seen.add(c.id)
                unique_candidates.append(c)

        print(f"\nCelkem unikátních kandidátů: {len(unique_candidates)}")
        
        recommended = Recommender.recommend_from_read(read_books, unique_candidates, count=15)
        print(f"\nDoporučeno: {len(recommended)}")
        for r in recommended:
            print(f"  - {r.title}")
        
        self.show_books(recommended)

    def add_to_read(self):
        if not self.current_book:
            self.result.setText("Nejprve si nech doporučit knihu.")
            return

        Storage.save_read_book(self.current_book)
        self.result.setText("Kniha byla přidána do přečtených.")


    def test_api_connection(self):
        google_ok = GoogleBooksAPI.test_connection()
        open_lib_ok = OpenLibraryAPI.test_connection()
    
        if google_ok or open_lib_ok:
            message = "Připojení OK!\n"
            if google_ok:
                message += "✓ Google Books API\n"
            if open_lib_ok:
                message += "✓ Open Library API\n"
            print(self, "Připojení", message)
        else:
            print(self, "Chyba", "Žádné API není dostupné!")