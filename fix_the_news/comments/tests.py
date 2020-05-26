from django.test import TestCase

from django_dynamic_fixture import G

from fix_the_news.comments import models
from fix_the_news.news_items import models as news_items_models


class TestCommentGenericRelations(TestCase):

    def test_adding_generic_relation(self):
        comment_text = 'this is a comment'
        comment = G(models.Comment, text=comment_text)
        news_item_title = 'this is a news item'
        news_item = G(news_items_models.NewsItem, title=news_item_title)
        news_item.comments.add(comment)

        self.assertEqual(news_item.comments.first().text, comment_text)
        self.assertEqual(comment.content_object.title, news_item_title)

    def test_add_comments_to_a_comment(self):
        comment = G(models.Comment)
        comment_text = 'this is a comment'
        another_comment = G(models.Comment, text=comment_text)
        comment.comments.add(another_comment)

        self.assertEqual(comment.comments.first().text, comment_text)
