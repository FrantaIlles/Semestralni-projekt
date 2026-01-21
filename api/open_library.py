import requests
from models.book import Book

class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org/search.json"
    
    @staticmethod
    def test_connection(timeout=5) -> bool:
        try:
            response = requests.get(
                OpenLibraryAPI.BASE_URL,
                params={"title": "test"},
                timeout=timeout
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def search(query, category=None, max_results=40):
        params = {
            "q": query,
            "limit": max_results
        }
        
        if category:
            params["q"] = f"{query} subject:{category}"

        response = requests.get(OpenLibraryAPI.BASE_URL, params=params)
        data = response.json()

        if "docs" not in data:
            return []
        
        books = []
        for item in data["docs"]:
            book = Book(
                id=item.get("key", ""),
                title=item.get("title", ""),
                authors=item.get("author_name", []),
                categories=item.get("subject", [])[:5],
                description="",
                pageCount=item.get("number_of_pages_median"),
                thumbnail=f"https://covers.openlibrary.org/b/id/{item.get('cover_i')}-S.jpg" if item.get("cover_i") else None
            )
            books.append(book)
        
        return books