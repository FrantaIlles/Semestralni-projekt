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
    def recommend_from_read(read_books, candidates, count=5):
        # ID již přečtených knih
        read_ids = {book.id for book in read_books}
        
        scored_books = []
        
        for c in candidates:
            # Přeskočit již přečtené knihy
            if c.id in read_ids:
                continue
                
            score = sum(Recommender.similarity(r, c) for r in read_books)
            scored_books.append((c, score))
        
        # Seřadit podle skóre a vrátit top N
        scored_books.sort(key=lambda x: x[1], reverse=True)
        return [book for book, score in scored_books[:count]]
    
    @staticmethod
    def recommend_from_params(books,min_pages=None, count=5):
        results = []
        
        for b in books:

            if min_pages and (not b.pageCount or b.pageCount < min_pages):
                continue

            results.append(b)
            
            if len(results) >= count:
                break
        
        return results