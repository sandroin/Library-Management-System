from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from users.choices import Status
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', Status.librarian)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email Address'), unique=True)
    full_name = models.CharField(_('Full Name'), max_length=255)
    personal_number = models.CharField(_('Personal Number'), max_length=20, unique=True)
    birth_date = models.DateField(_('Birth Date'))
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.client)
    is_active = models.BooleanField(
        _('active'),
        default=False,
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'personal_number', 'birth_date']

    def is_client(self):
        return self.status == Status.client

    def is_librarian(self):
        return self.status == Status.librarian

    def __str__(self):
        return self.email
