from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from fix_the_news.users import models


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
            'subscribe_to_emails',
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
                'subscribe_to_emails',
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
        'subscribe_to_emails',
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


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'get_email',
        'type',
    )
    list_filter = (
        'type',
    )
    ordering = (
        'date_created',
    )
    search_fields = (
        'text',
        'title',
        'type',
        'user__email',
        'user__first_name',
        'user__last_name',
    )


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(models.Message, MessageAdmin)
