from django.contrib.auth.models import User
from django.db import connection
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .strategies import BookSuggestion, GenreBasedSuggestionStrategy

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
        books = [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in rows]
        return Response(books)

class AddReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        book_id = request.data.get('book_id')
        rating = request.data.get('rating')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reviews (book_id, user_id, rating) VALUES (%s, %s, %s)", [book_id, user_id, rating])
        return Response({"message": "Review added successfully"})

class UpdateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_id = request.user.id
        book_id = request.data.get('book_id')
        new_rating = request.data.get('rating')
        with connection.cursor() as cursor:
            cursor.execute("UPDATE reviews SET rating = %s WHERE user_id = %s AND book_id = %s", [new_rating, user_id, book_id])
        return Response({"message": "Review updated successfully"})

class DeleteReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = request.user.id
        book_id = request.data.get('book_id')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE user_id = %s AND book_id = %s", [user_id, book_id])
        return Response({"message": "Review deleted successfully"})

class GenreFilterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        genre = request.query_params.get('genre', None)
        if genre is None:
            return Response({"error": "Genre parameter is required"}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books WHERE genre = %s", [genre])
            rows = cursor.fetchall()

        books = [{'id': row[0], 'title': row[1], 'author': row[2], 'genre': row[3]} for row in rows]
        return Response(books)

class BookSuggestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        suggestion_system = BookSuggestion(GenreBasedSuggestionStrategy())
        suggestions = suggestion_system.suggest(request.user.id)
        return Response(suggestions)