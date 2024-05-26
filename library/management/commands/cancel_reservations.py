from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import Reservation


class Command(BaseCommand):
    help = 'Cancel expired reservations'

    def handle(self, *args, **kwargs):
        expired_reservations = Reservation.objects.filter(reserved=True, expiration_date__lt=timezone.now())
        for reservation in expired_reservations:
            reservation.reserved = False
            reservation.save()
        self.stdout.write(self.style.SUCCESS('Expired reservations canceled successfully.'))
