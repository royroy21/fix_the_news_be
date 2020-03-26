from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from fix_the_news.users.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': (
            'email',
            'username',
            'password',
            'last_login',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': (
                'wide',
            ),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
            ),
        }),
    )

    list_display = (
        'email',
        'username',
        'is_staff',
        'last_login',
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )
    search_fields = (
        'email',
        'username',
    )
    ordering = (
        'email',
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
    readonly_fields = (
    )


admin.site.register(User, UserAdmin)