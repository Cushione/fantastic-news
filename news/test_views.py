from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Article, Comment


class TestViewsWithoutArticles(TestCase):
    """
    Tests for Views if no Articles exist
    """

    def setUp(self):
        # Remove all Articles from the Database
        Article.objects.all().delete()

    def test_get_home_page_without_articles(self):
        response = self.client.get(reverse("news:home"))
        self.assertEqual(response.status_code, 500)

    def test_get_nonexisting_article(self):
        response = self.client.get(
            reverse("news:article_detail", args=["test-slug"])
        )
        self.assertEqual(response.status_code, 404)


class TestViews(TestCase):
    """
    Test Views with existing Articles
    """

    def setUp(self):
        # Create Test User
        user = User.objects.create_user(username="testuser", password="12345")
        # Create three Test Articles
        for i in range(3):
            Article.objects.create(
                title=f"Test Article {i}",
                slug=f"test-article-{i}",
                author=user,
                status=1,
                content="Test Content",
                location="Test Environment",
            )

    def tearDown(self):
        # Remove all Articles after testing
        Article.objects.all().delete()

    def test_get_home_page(self):
        response = self.client.get(reverse("news:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_get_article_detail(self):
        response = self.client.get(
            reverse("news:article_detail", args=["test-article-1"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_detail.html")


class TestMemberFeaturesAsAuthenticated(TestCase):
    """
    Test Member Features as authenticated User
    """

    def setUp(self):
        # Create Test User
        user = User.objects.create_user(username="testuser", password="12345")
        # Login Test User
        c = Client()
        self.client.login(username="testuser", password="12345")
        # Create three Test Articles
        for i in range(3):
            Article.objects.create(
                title=f"Test Article {i}",
                slug=f"test-article-{i}",
                author=user,
                status=1,
                content="Test Content",
                location="Test Environment",
            )
        # Create Test Comment
        article = Article.objects.get(slug="test-article-1")
        self.comment = Comment.objects.create(
            content="Test Comment", author=user, article=article
        )

    def test_can_add_comment_to_article(self):
        response = self.client.post(
            reverse("news:add_article_comment", args=["test-article-1"]),
            {"content": "Test Comment"},
        )
        self.assertRedirects(
            response, reverse("news:article_detail", args=["test-article-1"])
        )

    def test_can_like_and_unlike_article(self):
        response = self.client.post(
            reverse("news:article_like", args=["test-article-1"])
        )
        self.assertRedirects(
            response, reverse("news:article_detail", args=["test-article-1"])
        )
        article = Article.objects.get(slug="test-article-1")
        self.assertEqual(article.number_of_likes(), 1)
        response = self.client.post(
            reverse("news:article_like", args=["test-article-1"])
        )
        self.assertRedirects(
            response, reverse("news:article_detail", args=["test-article-1"])
        )
        self.assertEqual(article.number_of_likes(), 0)

    def test_can_edit_comment(self):
        response = self.client.post(
            reverse("news:article_comments", args=[self.comment.id]),
            {"content": "changed content"},
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.content, "changed content")

    def test_can_delete_comment(self):
        response = self.client.delete(
            reverse("news:article_comments", args=[self.comment.id])
        )
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.deleted, True)


class TestMemberFeaturesAsNotAuthenticated(TestCase):
    """
    Test Member Features as not authenticated User
    """

    def setUp(self):
        # Create Test User
        user = User.objects.create_user(username="testuser", password="12345")
        # Create three Test Articles
        for i in range(3):
            Article.objects.create(
                title=f"Test Article {i}",
                slug=f"test-article-{i}",
                author=user,
                status=1,
                content="Test Content",
                location="Test Environment",
            )
        # Create Test Comment
        article = Article.objects.get(slug="test-article-1")
        self.comment = Comment.objects.create(
            content="Test Comment", author=user, article=article
        )

    def test_can_not_add_comment_to_article(self):
        response = self.client.post(
            reverse("news:add_article_comment", args=["test-article-1"]),
            {"content": "Test Comment"},
        )
        next = reverse("news:add_article_comment", args=["test-article-1"])
        self.assertRedirects(
            response, reverse("member:login") + f"?next={next}"
        )

    def test_can_not_like_and_unlike_article(self):
        response = self.client.post(
            reverse("news:article_like", args=["test-article-1"])
        )
        next = reverse("news:article_like", args=["test-article-1"])
        self.assertRedirects(
            response, reverse("member:login") + f"?next={next}"
        )
        article = Article.objects.get(slug="test-article-1")
        self.assertEqual(article.number_of_likes(), 0)

    def test_can_not_edit_comment(self):
        response = self.client.post(
            reverse("news:article_comments", args=[self.comment.id]),
            {"content": "changed content"},
        )
        next = reverse("news:article_comments", args=[self.comment.id])
        self.assertRedirects(
            response, reverse("member:login") + f"?next={next}"
        )
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.content, "Test Comment")

    def test_can_not_delete_comment(self):
        response = self.client.delete(
            reverse("news:article_comments", args=[self.comment.id])
        )
        next = reverse("news:article_comments", args=[self.comment.id])
        self.assertRedirects(
            response, reverse("member:login") + f"?next={next}"
        )
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.deleted, False)


class TestCommentsAsNotOwner(TestCase):
    """
    Test Comments as authenticated User but not Author
    """

    def setUp(self):
        # Create Test User 1
        user1 = User.objects.create_user(
            username="testuser1", password="12345"
        )
        # Create Test User 2
        user2 = User.objects.create_user(
            username="testuser2", password="12345"
        )
        # Login Test User 1
        c = Client()
        self.client.login(username="testuser1", password="12345")
        # Create three Test Articles with Test User 2
        for i in range(3):
            Article.objects.create(
                title=f"Test Article {i}",
                slug=f"test-article-{i}",
                author=user2,
                status=1,
                content="Test Content",
                location="Test Environment",
            )
        # Create Test Comment
        article = Article.objects.get(slug="test-article-1")
        self.comment = Comment.objects.create(
            content="Test Comment", author=user2, article=article
        )

    def test_can_not_edit_comment(self):
        response = self.client.post(
            reverse("news:article_comments", args=[self.comment.id]),
            {"content": "changed content"},
        )
        self.assertEqual(response.status_code, 403)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.content, "Test Comment")

    def test_can_not_delete_comment(self):
        response = self.client.delete(
            reverse("news:article_comments", args=[self.comment.id])
        )
        self.assertEqual(response.status_code, 403)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.deleted, False)
