from rest_framework.routers import DefaultRouter
from fix_the_news.api.news_items import views as news_items_views

api_router = DefaultRouter()
api_router.register(r'news-types', news_items_views.NewsTypeViewSet)
