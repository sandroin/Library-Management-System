from django.core.management.base import BaseCommand
from library.models import Reservation
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


class Command(BaseCommand):
    help = 'Allow reservation once possible and send email notifications.'

    def handle(self, *args, **kwargs):
        wishes = Reservation.objects.filter(wishlist=True)

        for wish in wishes:
            book = wish.book
            if book.available_quantity() > 0:
                wish.reserved = True
                wish.wishlist = False
                wish.expiration_date = timezone.now() + timezone.timedelta(days=1)
                wish.save()

                subject = 'One of the books from your wishlist is ready for reservation.'
                message = f"Hello {wish.borrower.full_name},\n\nGood news! The book '{book.title}' from your wishlist\
                 is automatically reserved. The reservation is valid for 24 hours!"

                recipient_list = [wish.borrower.email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
