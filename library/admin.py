from django.contrib import admin
from library.models import *


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0
    fields = ('borrower', 'issued', 'issued_at', 'returned', 'return_date')
    readonly_fields = ('borrower', 'issued', 'issued_at', 'returned', 'return_date')
    can_delete = False


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    fields = ('borrower', 'reserved', 'reservation_date', 'expiration_date')
    readonly_fields = ('borrower', 'reserved', 'reservation_date', 'expiration_date')
    can_delete = False


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'get_genres', 'publication_date', 'quantity')
    list_filter = ('author', 'genres', 'publication_date')
    search_fields = ('title', 'author__name', 'genres__name')
    inlines = [IssueInline, ReservationInline]

    readonly_fields = ('issued_count', 'available_count', 'currently_issued_count')

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'

    def issued_count(self, obj):
        return Issue.objects.filter(book=obj).count()
    issued_count.short_description = 'Times Issued'

    def available_count(self, obj):
        total_issued = Issue.objects.filter(book=obj, returned=False).count()
        return obj.quantity - total_issued
    available_count.short_description = 'Available Copies'

    def currently_issued_count(self, obj):
        return Issue.objects.filter(book=obj, returned=False).count()
    currently_issued_count.short_description = 'Currently Issued'


admin.site.register(Book, BookAdmin)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id', 'name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'book', 'issued', 'issued_at', 'returned', 'return_date')
    search_fields = ('borrower__username', 'book__title')
    list_filter = ('issued', 'returned')
    date_hierarchy = 'issued_at'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'borrower', 'reservation_date', 'expiration_date', 'reserved', 'wishlist')
    search_fields = ('borrower__username', 'book__title')
    list_filter = ('reserved', 'wishlist')
    date_hierarchy = 'reservation_date'
