from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework import status
from rest_framework.test import APIClient

from fix_the_news.likes import models
from fix_the_news.users import models as users_models


class TestLikeViewSet(TestCase):

    def setUp(self):
        self.authenticated_client = APIClient()
        self.user = G(users_models.User)
        self.authenticated_client.force_authenticate(user=self.user)

    def test_delete_own_like(self):
        like = G(models.Like, user=self.user)
        endpoint = reverse('like-detail', kwargs={'pk': like.id})
        response = self.authenticated_client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_someone_elses_like(self):
        like = G(models.Like, user=G(users_models.User))
        endpoint = reverse('like-detail', kwargs={'pk': like.id})
        response = self.authenticated_client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
