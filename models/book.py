class Book:
    def __init__(self, id, title, authors, categories, description, pageCount, thumbnail=None):
        self.id = id
        self.title = title
        self.authors = authors or []
        self.categories = categories or []
        self.description = description or ""
        self.pageCount = pageCount
        self.thumbnail = thumbnail

    @staticmethod
    def from_api(item):
        info = item.get("volumeInfo", {})
        return Book(
            id=item.get("id"),
            title=info.get("title"),
            authors=info.get("authors"),
            categories=info.get("categories"),
            description=info.get("description"),
            pageCount=info.get("pageCount"),
            thumbnail=info.get("imageLinks", {}).get("thumbnail")
        )