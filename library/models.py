from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Author ID'))
    name = models.CharField(max_length=100, verbose_name=_('Author Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name=(_('Genre Name')))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Book(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('Book ID'))
    title = models.CharField(max_length=100, verbose_name=_('Book Title'))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('Author'))
    genres = models.ManyToManyField(Genre, verbose_name=_('Genre'))
    publication_date = models.DateField(verbose_name=_('Publication Date'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))

    def available_quantity(self):
        issued_count = self.issue_set.filter(issued=True, returned=False).count()
        reserved_count = self.reservation_set.filter(reserved=True).count()
        return self.quantity - issued_count - reserved_count

    def __str__(self):
        return self.title + " by " + str(self.author)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class Issue(models.Model):
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Borrower'))
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    issued = models.BooleanField(default=False, verbose_name=_('Is Issued'))
    issued_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Is Issued At'))
    returned = models.BooleanField(default=False, verbose_name=_('Is Returned'))
    return_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Returned Date'))

    def __str__(self):
        return f"{self.book.title} issued to {self.borrower.full_name}"

    class Meta:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"


class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_('Book'))
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Borrower'))
    reservation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Reservation Date'))
    expiration_date = models.DateTimeField(verbose_name=_('Expiration Date'))
    reserved = models.BooleanField(default=False, verbose_name=_('Is Reserved'))
    wishlist = models.BooleanField(default=False, verbose_name=_('Is In Wishlist'))

    def __str__(self):
        return f"{self.book.title} reserved by {self.borrower.username}"

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
