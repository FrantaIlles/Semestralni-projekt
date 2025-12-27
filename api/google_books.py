import requests
from models.book import Book

class GoogleBooksAPI:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    
    @staticmethod
    def test_connection(timeout=5) -> bool:
        try:
            response = requests.get(
                GoogleBooksAPI.BASE_URL,
                params={"q": "test"},
                timeout=timeout
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def search(query, lang=None, max_results=40):
        params = {
            "q": query,
            "maxResults": max_results
        }
        
        if lang:
            params["langRestrict"] = lang

        response = requests.get(GoogleBooksAPI.BASE_URL, params=params)
        data = response.json()

        if "items" not in data:
            return []
        
        return [Book.from_api(item) for item in data["items"]]