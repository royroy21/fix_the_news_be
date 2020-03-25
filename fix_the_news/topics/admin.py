from django.contrib import admin

from fix_the_news.topics import models


class CategoryAdmin(admin.ModelAdmin):
    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
        "type",
        "user__email",
        "user__username",
    )


class TopicAdmin(admin.ModelAdmin):
    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
        "user__email",
        "user__username",
    )


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Topic, TopicAdmin)
