from django.core.management.base import BaseCommand
from random import choice, randint
from datetime import datetime, timedelta
from library.models import Author, Genre, Book
from django.db import transaction


class Command(BaseCommand):
    help = 'Generate random books'

    def handle(self, *args, **kwargs):
        authors = list(Author.objects.all())
        genres = list(Genre.objects.all())

        total_books = 1000
        self.create_books(total_books, authors, genres)

    @transaction.atomic
    def create_books(self, number_of_books, authors, genres):
        books_to_create = []
        genres_to_assign = []

        for _ in range(number_of_books):
            title, author = self.generate_unique_book(authors)
            publication_date = datetime.now() - timedelta(days=randint(0, 3650))
            quantity = randint(1, 10)
            new_book = Book(
                title=title,
                author=author,
                publication_date=publication_date,
                quantity=quantity
            )
            books_to_create.append(new_book)

        created_books = Book.objects.bulk_create(books_to_create, batch_size=100)

        for book in created_books:
            genres_to_assign.append((book, self.random_genres(genres)))

        # Assign genres to books in batches
        for book, genre_list in genres_to_assign:
            book.genres.set(genre_list)

    def generate_unique_book(self, authors):
        while True:
            title = self.generate_book_title()
            author = choice(authors)
            if not Book.objects.filter(title=title, author=author).exists():
                return title, author

    def generate_book_title(self):
        adjectives = ['Dark', 'Mystery', 'Silent', 'Ancient', 'Broken', 'Shattered', 'Secret']
        nouns = ['Shadows', 'Dreams', 'Empire', 'Journey', 'Whispers', 'Legacy', 'Storm']
        return f"{choice(adjectives)} {choice(nouns)}"

    def random_genres(self, genres):
        return [choice(genres) for _ in range(randint(1, 3))]
