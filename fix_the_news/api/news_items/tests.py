from django_dynamic_fixture import G
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from fix_the_news.news_items import models
from fix_the_news.topics import models as topics_models
from fix_the_news.users import models as users_models


class TestNewsItemViewSet(TestCase):

    list_endpoint = reverse("newsitem-list")

    def setUp(self):
        self.unauthenticated_client = APIClient()
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=G(users_models.User))

        self.topic = G(topics_models.Topic)
        self.for_category = G(
            topics_models.Category,
            type=topics_models.Category.TYPE_FOR,
            topic=self.topic,
        )
        self.neutral_category = G(
            topics_models.Category,
            type=topics_models.Category.TYPE_NEUTRAL,
            topic=self.topic,
        )
        self.against_category = G(
            topics_models.Category,
            type=topics_models.Category.TYPE_AGAINST,
            topic=self.topic,
        )
        self.news_type = G(models.NewsType)
        self.for_news_item = G(
            models.NewsItem,
            category=self.for_category,
            title="This news item is for",
            type=self.news_type,
        )
        self.neutral_news_item = G(
            models.NewsItem,
            category=self.neutral_category,
            title="This news item is neutral",
            type=self.news_type,
        )
        self.against_news_item = G(
            models.NewsItem,
            category=self.against_category,
            title="This news item is against",
            type=self.news_type,
        )

    def test_no_filters(self):
        response = self.unauthenticated_client.get(self.list_endpoint)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)

    def test_filter_for_category_news_items(self):
        params = {"for": True}
        response = self.unauthenticated_client.get(self.list_endpoint, params)
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], self.for_news_item.title)

    def test_filter_for_and_against_category_news_items(self):
        params = {"for": True, "against": True}
        response = self.unauthenticated_client.get(self.list_endpoint, params)

        self.assertEqual(response.status_code, 200)

        results = response.json()["results"]
        self.assertEqual(len(results), 2)

        response_titles = sorted([
            news_item["title"]
            for news_item
            in results
        ])
        expected_titles = sorted([
            self.for_news_item.title,
            self.against_news_item.title,
        ])
        self.assertEqual(response_titles, expected_titles)

    def test_delete(self):
        # Users should not be able to delete news items
        detail_endpoint = \
            reverse("newsitem-detail", kwargs={"pk": self.for_news_item})
        response = self.unauthenticated_client.delete(detail_endpoint)
        self.assertEqual(response.status_code, 404)
        news_item_exists = \
            models.NewsItem.objects.filter(id=self.for_news_item.id).exists()
        self.assertTrue(news_item_exists)

    def get_create_new_news_item_data(self):
        return {
            "title": "A new news item",
            "topic": self.topic.id,
            "type": self.news_type.id,
            "url": "www.news.com",
            "category": self.for_category.id,
        }

    def test_create_with_authenticated_user(self):
        data = self.get_create_new_news_item_data()
        response = \
            self.authenticated_client.post(self.list_endpoint, data=data)
        self.assertEqual(response.status_code, 201)
        news_item_exists = \
            models.NewsItem.objects.filter(title=data["title"]).exists()
        self.assertTrue(news_item_exists)

    def test_create_with_unauthenticated_user(self):
        data = self.get_create_new_news_item_data()
        response = \
            self.unauthenticated_client.post(self.list_endpoint, data=data)
        self.assertEqual(response.status_code, 401)
        news_item_exists = \
            models.NewsItem.objects.filter(title=data["title"]).exists()
        self.assertTrue(news_item_exists)
