from rest_framework.routers import DefaultRouter
from fix_the_news.api.news_items import views as news_items_views
from fix_the_news.api.topics import views as topics_views

api_router = DefaultRouter()
api_router.register(r'news-items', news_items_views.NewsItemViewSet)
api_router.register(r'news-types', news_items_views.NewsTypeViewSet)
api_router.register(r'topics', topics_views.TopicViewSet)
