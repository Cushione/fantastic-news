from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    Form for writing comments.
    """

    class Meta:
        model = Comment
        fields = ("content",)
