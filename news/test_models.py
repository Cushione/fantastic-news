from django.test import TestCase
from .views import Article, Comment
from django.contrib.auth.models import User


class TestArticleModel(TestCase):
    """
    Tests for the Article Model
    """

    def setUp(self):
        # Create Test User
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        # Create Test Article
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user,
            content="Test Content",
            location="Test Environment",
        )

    def test_published_on_defaults_to_null(self):
        article = Article.objects.get(title="Test Article")
        self.assertIsNone(article.published_on)

    def test_status_defaults_to_draft(self):
        article = Article.objects.get(title="Test Article")
        self.assertEqual(article.status, 0)

    def test_featured_image_defaults_to_placeholder(self):
        article = Article.objects.get(title="Test Article")
        self.assertIn("placeholder", article.featured_image.url)

    def test_article_has_number_of_likes(self):
        article = Article.objects.get(title="Test Article")
        self.assertEqual(article.number_of_likes(), 0)
        article.likes.add(self.user)
        self.assertEqual(article.number_of_likes(), 1)

    def test_article_has_number_of_comments(self):
        article = Article.objects.get(title="Test Article")
        self.assertEqual(article.number_of_comments(), 0)

    def test_article_string_representation(self):
        article = Article.objects.get(title="Test Article")
        self.assertEqual(str(article), "Test Article")

