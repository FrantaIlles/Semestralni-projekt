from api.google_books import GoogleBooksAPI
from api.open_library import OpenLibraryAPI

class CombinedSearch:
    @staticmethod
    def search(query, category=None, max_results=40):
        google_books = GoogleBooksAPI.search(query, max_results=max_results//2)
        open_library_books = OpenLibraryAPI.search(query, category=category, max_results=max_results//2)
        
        # Sloučit a odstranit duplikáty (podle názvu a autora)
        seen = set()
        combined = []
        
        for book in google_books + open_library_books:
            key = (book.title.lower(), tuple(sorted([a.lower() for a in book.authors])))
            
            if key not in seen:
                seen.add(key)
                combined.append(book)
        
        return combined[:max_results]
    
    @staticmethod
    def test_connection():
        google_ok = GoogleBooksAPI.test_connection()
        open_lib_ok = OpenLibraryAPI.test_connection()
        return google_ok or open_lib_ok  