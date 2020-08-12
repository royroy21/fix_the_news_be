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
        "user__first_name",
        "user__last_name",
    )


class TopicAdmin(admin.ModelAdmin):

    change_form_template = 'admin/topics/change_form.html'

    def response_change(self, request, obj):
        if "_top_rated" in request.POST:
            from fix_the_news.topics.services import scoring_service
            obj.score = \
                scoring_service.TopicScoringService().get_highest_score()
            obj.save()
        return super().response_change(request, obj)

    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
        "user__email",
        "user__first_name",
        "user__last_name",
    )


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Topic, TopicAdmin)
