import re
from api.google_books import GoogleBooksAPI
from api.open_library import OpenLibraryAPI

class CombinedSearch:
    @staticmethod
    def _norm_title(title: str) -> str:
        if not title:
            return ""
        t = title.lower().strip()
        t = re.sub(r"\s*\(.*?\)", "", t)   # odstraň text v závorkách
        t = re.split(r"[:\-]", t)[0]       # odřízni podtitul za : nebo -
        t = re.sub(r"\s+", " ", t)
        return t.strip()

    @staticmethod
    def search(query, category=None, max_results=40):
        try:
            google_books = GoogleBooksAPI.search(query, max_results=max_results//2)
        except Exception:
            google_books = []
        try:
            open_library_books = OpenLibraryAPI.search(query, category=category, max_results=max_results//2)
        except Exception:
            open_library_books = []
        
        seen_keys = set()
        seen_titles = set()
        combined = []

        for b in google_books + open_library_books:
            title_norm = CombinedSearch._norm_title(b.title)
            authors_norm = tuple(sorted([a.lower().strip() for a in (b.authors or [])]))
            key = (title_norm, authors_norm)

            # deduplikace stejné knihy (název + autoři)
            if key in seen_keys:
                continue
            # limituj na 1 kus stejného základního názvu (i když mají různé autory/překladatele)
            if title_norm in seen_titles:
                continue

            seen_keys.add(key)
            seen_titles.add(title_norm)
            combined.append(b)

        # stabilní řazení abecedně podle názvu
        #combined.sort(key=lambda x: (x.title or "").lower())
        return combined[:max_results]

    @staticmethod
    def test_connection():
        google_ok = GoogleBooksAPI.test_connection()
        open_lib_ok = OpenLibraryAPI.test_connection()
        return google_ok or open_lib_ok