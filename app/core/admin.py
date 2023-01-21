"""
Django Admin Customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """"Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


class CryptoAdmin(admin.ModelAdmin):
    """Define de admin pages for Crypto."""
    ordering=['date_and_time', 'symbol']
    list_display = (
        'date_and_time',
        'symbol',
        'open',
        'close',
        'volume',
        'low',
        'high',
    )
    list_filter = ['symbol']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Order)
admin.site.register(models.Crypto, CryptoAdmin)
