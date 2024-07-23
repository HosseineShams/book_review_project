from django.urls import path
from .views import (CreateUserView, BookListView, AddReviewView, UpdateReviewView, DeleteReviewView, GenreFilterView,
                    TokenObtainPairView, TokenRefreshView, BookSuggestionView)

urlpatterns = [
    path('api/register/', CreateUserView.as_view(), name='user-register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/book/list/', BookListView.as_view(), name='book-list'),
    path('api/review/add/', AddReviewView.as_view(), name='review-add'),
    path('api/review/update/', UpdateReviewView.as_view(), name='review-update'),
    path('api/review/delete/', DeleteReviewView.as_view(), name='review-delete'),
    path('api/book/', GenreFilterView.as_view(), name='book-filter'),
    path('api/books/suggestions/', BookSuggestionView.as_view(), name='book-suggestions'),
]
