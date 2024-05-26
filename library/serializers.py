from rest_framework import serializers
from library.models import *
from users.models import CustomUser


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    author_name = serializers.CharField(source='author.name', read_only=True)
    genres = serializers.SlugRelatedField(slug_field='name', queryset=Genre.objects.all(), many=True)
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', "author_name", 'genres', 'publication_date', 'quantity', 'available_quantity']

    def get_available_quantity(self, obj):
        return obj.available_quantity()


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author_name', 'genres', 'available_quantity']

    def get_available_quantity(self, obj):
        return obj.available_quantity()


class ReservationSerializer(serializers.ModelSerializer):
    borrower = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Reservation
        fields = ['borrower', 'book', 'reservation_date', 'expiration_date', 'reserved', 'wishlist']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

    def validate(self, data):
        if data.get('issued') and data.get('returned'):
            raise serializers.ValidationError("An issue cannot be both issued and returned at the same time.")
        return data


# ----------------------------------------------------------------------------------------------------------------------
# Statistics
class TopBooksSerializer(serializers.ModelSerializer):
    number_of_borrows = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'number_of_borrows']


class LastYearBorrowsSerializer(serializers.ModelSerializer):
    number_of_borrows = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'number_of_borrows']


class MostLateReturnsSerializer(serializers.ModelSerializer):
    late_returns = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'late_returns']


class LateReturnersSerializer(serializers.ModelSerializer):
    late_returns = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'late_returns']
