from django.core.management.base import BaseCommand
from faker import Faker
from library.models import Author


class Command(BaseCommand):
    help = 'Generate 100 random authors'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(100):
            name = fake.name()
            Author.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS('Successfully generated 100 random authors.'))
