from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Form for registring new members.
    Extends default user creation form by first name and email address.
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        help_text="50 characters or fewer."
        )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
