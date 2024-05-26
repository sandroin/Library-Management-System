import math
from collections import OrderedDict
from datetime import timedelta, datetime
from django.db.models import Q, Count, F
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import generics, filters, viewsets, status, pagination, permissions
from rest_framework.response import Response
from library.serializers import *
from django_filters.rest_framework import DjangoFilterBackend


def index(request):
    return render(request, 'index.html')


class IsStaffMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class CustomPageNumber(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('last_page', math.ceil(self.page.paginator.count / self.page_size)),
             ('results', data)
         ]))


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsStaffMember]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsStaffMember]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPageNumber
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genres']
    search_fields = ['title', 'author__name', 'genres__name']
    ordering_fields = ['title', 'author__name', 'publication_date']
    permission_classes = [IsStaffMember]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['book__title', 'borrower__email']
    ordering_fields = ['issued', 'issued_at', 'returned_at']
    permission_classes = [IsStaffMember]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')

        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.available_quantity() <= 0:
            return Response({"error": "No available copies of the book"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['book__title', 'borrower__email']
    filterset_fields = ['reserved', 'reservation_date']
    permission_classes = [IsStaffMember]

    def create(self, request, *args, **kwargs):
        user = request.user
        book_id = request.data.get('book_id')

        if not book_id:
            book_id = request.data.get('book')

        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        available_copies = book.available_quantity()

        if available_copies > 0:
            reserved = True
            wishlist = False
        else:
            reserved = False
            wishlist = True

        expiration_date = datetime.now() + timedelta(days=1)

        data = {
            "borrower": user.id,
            "book": book.id,
            "expiration_date": expiration_date,
            "reserved": reserved,
            "wishlist": wishlist
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookListView(TemplateView):
    template_name = 'library/book_list.html'


class BookDetailView(TemplateView):
    template_name = 'library/book_detail.html'


# ----------------------------------------------------------------------------------------------------------------------
# Statistics


class TopTenBooks(generics.ListAPIView):
    serializer_class = TopBooksSerializer
    permission_classes = [IsStaffMember]

    def get_queryset(self):
        return Book.objects.annotate(
            number_of_borrows=Count('issue', filter=Q(issue__issued=True))).order_by('-number_of_borrows')[:10]


class BorrowsLastYear(generics.ListAPIView):
    serializer_class = LastYearBorrowsSerializer
    permission_classes = [IsStaffMember]

    def get_queryset(self):
        return Book.objects.annotate(number_of_borrows=Count('issue',
                filter=Q(issue__issued_at__gte=timezone.now() - timedelta(days=365)))).order_by('-number_of_borrows')


class MostLateReturns(generics.ListAPIView):
    serializer_class = MostLateReturnsSerializer
    permission_classes = [IsStaffMember]

    def get_queryset(self):
        return Book.objects.annotate(late_returns=Count('issue',
                filter=Q(issue__returned=True) & Q(issue__return_date__gt=F('issue__issued_at') +
                                    timedelta(days=14)))).order_by('-late_returns')[:100]


class UsersWithMostLateReturns(generics.ListAPIView):
    serializer_class = LateReturnersSerializer
    permission_classes = [IsStaffMember]

    def get_queryset(self):
        return CustomUser.objects.annotate(late_returns=Count('issue',
                filter=Q(issue__returned=True) & Q(issue__return_date__gt=F('issue__issued_at') +
                        timedelta(days=14)))).order_by('-late_returns')[:100]
