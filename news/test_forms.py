from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):

    def test_comment_content_is_required(self):
        form = CommentForm({'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors.keys()) 