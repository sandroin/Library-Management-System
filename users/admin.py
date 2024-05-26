from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'personal_number', 'birth_date')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'status', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'personal_number', 'birth_date', 'password1', 'password2', 'status', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'status')
    search_fields = ('full_name', 'personal_number', 'email')
    list_display = ('email', 'full_name', 'personal_number', 'birth_date', 'is_staff', 'is_active')
    ordering = ['email']