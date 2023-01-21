from django.test import TestCase
from .forms import CommentForm


class TestCommentForm(TestCase):
    """
    Tests for the "Add Comment Form"
    """
    def test_comment_content_is_required(self):
        form = CommentForm({'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors.keys()) 

    def test_fields_are_explicit_in_form_metaclass(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('content',))