from django.contrib import admin

from fix_the_news.topics import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "title",
        "topic",
        "user",
    )
    list_filter = (
        "topic__title",
    )
    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
        "type",
        "user__email",
        "user__first_name",
        "user__last_name",
    )


class TopicAdmin(admin.ModelAdmin):

    change_form_template = 'admin/topics/change_form.html'

    def response_change(self, request, obj):
        if '_top_rated' in request.POST:
            from fix_the_news.topics.services import scoring_service
            obj.score = \
                scoring_service.TopicScoringService().get_highest_score()
            obj.save()
        if '_calculate_score' in request.POST:
            obj.save_score()
        return super().response_change(request, obj)

    list_display = (
        "title",
        "user",
        "score",
        "priority",
        "date_created",
    )
    list_filter = (
        "priority",
    )
    ordering = (
        "-priority",
        "-score",
        "-date_created",
    )
    search_fields = (
        "title",
        "title__startswith",
        "user__email",
        "user__first_name",
        "user__last_name",
    )


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Topic, TopicAdmin)
