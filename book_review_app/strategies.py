from django.db import connection

class SuggestionStrategy:
    def suggest_books(self, user_id):
        raise NotImplementedError("Subclasses must implement this method.")

class GenreBasedSuggestionStrategy(SuggestionStrategy):
    def suggest_books(self, user_id):
        # Find the user's favorite genre based on past highest ratings
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT genre, COUNT(genre) as genre_count
                FROM books
                JOIN reviews ON books.id = reviews.book_id
                WHERE reviews.user_id = %s AND rating = 5
                GROUP BY genre
                ORDER BY genre_count DESC
                LIMIT 1
            """, [user_id])
            result = cursor.fetchone()
            if not result:
                return []
            favorite_genre = result[0]

        # Suggest books from the favorite genre that the user has not rated yet
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, author, genre
                FROM books
                WHERE genre = %s AND id NOT IN (
                    SELECT book_id FROM reviews WHERE user_id = %s
                )
            """, [favorite_genre, user_id])
            rows = cursor.fetchall()

        return [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in rows]

class BookSuggestion:
    def __init__(self, strategy: SuggestionStrategy):
        self.strategy = strategy

    def suggest(self, user_id):
        return self.strategy.suggest_books(user_id)