from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Article, Comment

class TestViewsWithoutArticles(TestCase):
    def setUp(self):
        Article.objects.all().delete()

    def test_get_home_page_without_articles(self):
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, 500)
    
    def test_get_nonexisting_article(self):
        response = self.client.get(reverse('news:article_detail', args=["test-slug"]))
        self.assertEqual(response.status_code, 404)

class TestViews(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        for i in range(3):
            Article.objects.create(
                title=f"Test Article {i}", 
                slug=f"test-article-{i}",
                author=user,
                status=1,
                content="Test Content",
                location="Test Environment"
                )
    
    def tearDown(self):
        Article.objects.all().delete()

    def test_get_home_page(self):    
        response = self.client.get(reverse('news:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_get_article_detail(self):
        response = self.client.get(reverse('news:article_detail', args=["test-article-1"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')


class TestMemberFeatures(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        c = Client()
        self.client.login(username='testuser', password='12345')
        for i in range(3):
            Article.objects.create(
                title=f"Test Article {i}", 
                slug=f"test-article-{i}",
                author=user,
                status=1,
                content="Test Content",
                location="Test Environment"
                )
        article = Article.objects.get(slug="test-article-1")
        self.comment = Comment.objects.create(
            content="Test Comment",
            author=user,
            article=article
        )
    
    def test_can_add_comment_to_article(self):
        response = self.client.post(reverse('news:article_detail', args=["test-article-1"]), {'content': 'Test Comment'})
        self.assertRedirects(response, reverse('news:article_detail', args=["test-article-1"]))
    
    def test_can_like_and_unlike_article(self):
        response = self.client.post(reverse('news:article_like', args=["test-article-1"]))
        self.assertRedirects(response, reverse('news:article_detail', args=["test-article-1"]))
        article = Article.objects.get(slug="test-article-1")
        self.assertEqual(article.number_of_likes(), 1)
        response = self.client.post(reverse('news:article_like', args=["test-article-1"]))
        self.assertRedirects(response, reverse('news:article_detail', args=["test-article-1"]))
        self.assertEqual(article.number_of_likes(), 0)

    def test_can_edit_comment(self):
        response = self.client.post(reverse('news:article_comments', args=[self.comment.id]), {'content': 'changed content'})
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.content, 'changed content')

    def test_can_delete_comment(self):
        response = self.client.delete(reverse('news:article_comments', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.deleted, True)