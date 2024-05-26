from django.urls import path
from library import views
from rest_framework.routers import DefaultRouter
from library.views import *

router = DefaultRouter()
router.register('api/books', BookViewSet, basename='book')
router.register('api/authors', AuthorViewSet, basename='author')
router.register('api/genres', GenreViewSet, basename='genre')
router.register('api/issues', IssueViewSet, basename='issue')
router.register('api/reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/top-books/', TopTenBooks.as_view(), name='top_books'),
    path('api/borrows-last-year/', BorrowsLastYear.as_view(), name='borrows_last_year'),
    path('api/most-late-returns/', MostLateReturns.as_view(), name='most_late_returns'),
    path('api/late-returners/', UsersWithMostLateReturns.as_view(), name='late_returners'),
    path('book-list/', BookListView.as_view(), name='book_list'),
    path('book-list/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]

urlpatterns += router.urls
