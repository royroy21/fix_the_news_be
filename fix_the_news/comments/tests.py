from django.test import TestCase

from django_dynamic_fixture import G

from fix_the_news.comments import models
from fix_the_news.news_items import models as news_items_models


class TestCommentGenericRelations(TestCase):

    def setUp(self):
        self.comment_text = 'this is a comment'
        self.comment = G(
            models.Comment,
            text=self.comment_text,
        )
        self.news_item_title = 'this is a news item'
        self.news_item = G(
            news_items_models.NewsItem,
            title=self.news_item_title,
        )

    def test_add_by_generic_relation(self):
        self.news_item.comments.add(self.comment)

        self.assertEqual(
            self.news_item.comments.first().text,
            self.comment_text,
        )
        self.assertEqual(
            self.comment.content_object.title,
            self.news_item_title,
        )

    def test_add_by_content_object(self):
        self.comment.content_object = self.news_item
        self.comment.save()

        self.assertEqual(
            self.news_item.comments.first().text,
            self.comment_text,
        )
        self.assertEqual(
            self.comment.content_object.title,
            self.news_item_title,
        )

    def test_add_comments_to_a_comment(self):
        another_comment = G(models.Comment, text=self.comment_text)
        self.comment.comments.add(another_comment)

        self.assertEqual(
            self.comment.comments.first().text,
            self.comment_text,
        )
