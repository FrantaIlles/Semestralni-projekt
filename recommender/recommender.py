class Recommender:
    @staticmethod
    def similarity(b1, b2):
        score = 0

        if b1.categories and b2.categories:
            score += len(set(b1.categories) & set(b2.categories)) * 5

        if b1.authors and b2.authors:
            score += len(set(b1.authors) & set(b2.authors)) * 20

        if b1.pageCount and b2.pageCount:
            if abs(b1.pageCount - b2.pageCount) <= 30:
                score += 3
        
        # Bonus za podobný název (detekce série)
        if b1.title and b2.title:
            # Rozdělení názvu na slova a porovnání
            words1 = set(b1.title.lower().split())
            words2 = set(b2.title.lower().split())
            common_words = words1 & words2
            # Ignorovat krátká slova (and, the, etc.)
            meaningful_common = [w for w in common_words if len(w) > 3]
            if meaningful_common:
                score += len(meaningful_common) * 15

        return score
    
    @staticmethod
    def recommend_from_read(read_books, candidates):
        best_book = None
        best_score = -1
        
        # ID již přečtených knih
        read_ids = {book.id for book in read_books}

        for c in candidates:
            # Přeskočit již přečtené knihy
            if c.id in read_ids:
                continue
                
            score = sum(Recommender.similarity(r, c) for r in read_books)

            if score > best_score:
                best_score = score
                best_book = c

        return best_book
    
    @staticmethod
    def recommend_from_params(books, category=None, author=None, min_pages=None):

        for b in books:

            if category and (not b.categories or not any(category.lower() in cat.lower() for cat in b.categories)):
                continue

            if author and (not b.authors or not any(author.lower() in aut.lower() for aut in b.authors)):
                continue

            if min_pages and (not b.pageCount or b.pageCount < min_pages):
                continue

            return b
        
        return None