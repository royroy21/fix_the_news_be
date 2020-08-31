from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': (
            'email',
            'first_name',
            'last_name',
            'password',
            'last_login',
            'has_viewed_registration_communication',
            'has_viewed_daily_communication',
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
                'first_name',
                'last_name',
                'password1',
                'password2',
                'has_viewed_registration_communication',
                'has_viewed_daily_communication',
            ),
        }),
    )

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'last_login',
        'has_viewed_registration_communication',
        'has_viewed_daily_communication',
    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
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


admin.site.register(get_user_model(), UserAdmin)
