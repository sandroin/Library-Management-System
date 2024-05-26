from django.core.management.base import BaseCommand
from library.models import Issue
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Handles expired issues'

    def handle(self, *args, **kwargs):
        expired_issues = Issue.objects.filter(
            issued=True,
            returned=False,
            issued_at__lt=timezone.now() - timezone.timedelta(days=14)
        )

        for issue in expired_issues:
            subject = 'Expired Issue'
            message = ("Hello {issue.borrower.full_name},\n\nThis is a reminder that your borrowed book, \
                       {issue.book.title}, is now overdue. Please return it to the library at your earliest \
                        convenience to avoid any penalties.\n\n")
            recipient_list = [issue.borrower.email]
            print(recipient_list)
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
