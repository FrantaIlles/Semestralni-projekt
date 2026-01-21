class Recommender:
    @staticmethod
    def similarity(b1, b2):
        if b1.id == b2.id:
            return 0
        score = 0
        
        # Kategorie (přímé porovnání)
        if b1.categories and b2.categories:
            common_cat = set(b1.categories) & set(b2.categories)
            score += len(common_cat) * 10

        # Autoři (přímé porovnání)
        if b1.authors and b2.authors:
            common_auth = set(b1.authors) & set(b2.authors)
            score += len(common_auth) * 20

        # Počet stran
        if b1.pageCount and b2.pageCount:
            diff = abs(b1.pageCount - b2.pageCount)
            if diff <= 30:
                score += 15
            elif diff <= 60:
                score += 8

        # Podobnost názvu (společná slova > 3 znaky)
        if b1.title and b2.title:
            w1 = {w.lower() for w in b1.title.split() if len(w) > 3}
            w2 = {w.lower() for w in b2.title.split() if len(w) > 3}
            common_words = w1 & w2
            score += len(common_words) * 6
            # Série / stejné první slovo
            t1 = b1.title.split()[0].lower()
            t2 = b2.title.split()[0].lower()
            if t1 == t2:
                score += 10

        return score
    
    @staticmethod
    def recommend_from_read(read_books, candidates, count=5):
        read_ids = {book.id for book in read_books}
        read_titles = {book.title.lower().strip() for book in read_books if book.title}
        
        # Spočítej kolikrát se každý autor objevuje v přečtených knihách
        author_counts = {}
        for b in read_books:
            if b.authors:
                for author in b.authors:
                    author_counts[author] = author_counts.get(author, 0) + 1
        
        scored_books = []
        seen_titles = set()

        for c in candidates:
            if c.id in read_ids:
                continue
            
            title_norm = c.title.lower().strip() if c.title else ""
            
            if title_norm in read_titles:
                continue
            if title_norm in seen_titles:
                continue
            seen_titles.add(title_norm)
            
            total_score = sum(Recommender.similarity(r, c) for r in read_books)
            
            # BONUS: progresivní bodování podle počtu přečtených knih od autora
            if c.authors:
                for author in c.authors:
                    if author in author_counts:
                        # Čím víc knih od autora, tím víc bodů (15 za první, +5 za každou další)
                        bonus = 15 + (author_counts[author] - 1) * 5
                        total_score += bonus
            
            if total_score > 0:
                scored_books.append((c, total_score))

        scored_books.sort(key=lambda x: x[1], reverse=True)
        return [book for book, score in scored_books[:count]]
    
    @staticmethod
    def recommend_from_params(books, min_pages=None, count=5):
        results = []
        for b in books:
            if min_pages and (not b.pageCount or b.pageCount < min_pages):
                continue
            results.append(b)
            if len(results) >= count:
                break
        return results