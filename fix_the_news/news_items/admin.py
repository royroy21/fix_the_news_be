from django.contrib import admin

from fix_the_news.news_items import models


class NewsItemAdmin(admin.ModelAdmin):
    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
        "topic__title"
        "type__title",
        "user__email",
        "user__username",
        "url",
        "category__title",
    )


class NewsTypeAdmin(admin.ModelAdmin):
    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
    )


admin.site.register(models.NewsItem, NewsItemAdmin)
admin.site.register(models.NewsType, NewsTypeAdmin)
