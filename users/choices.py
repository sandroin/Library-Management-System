from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class Status(IntegerChoices):
    librarian = 1, _("Librarian")
    client = 2, _("Client")
