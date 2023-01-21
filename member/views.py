from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def login_request(request):
    """
    Login Function Based View for logging in users.
    """
    # If the user is already authenticated, redirect to the homepage
    # or the previous page if applicable
    if request.user.is_authenticated:
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        else:
            return redirect("news:home")
    form = AuthenticationForm()
    # Attempt login on POST request
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        # If the form is valid, authenticate the user and on success login
        # the user. Redirect to the homepage or the previous page
        # if applicable
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("news:home")
        # If the form is invalid or the user could not be authenticated, add
        # error message
        messages.error(request, "Invalid username or password.")
    # Send empty form on GET request and form with errors if login failed
    return render(
        request, template_name="login.html", context={"login_form": form}
    )


def register_request(request):
    """
    Register Function Based View for registrating users.
    """
    # If the user is already authenticated, redirect to the homepage
    # or the previous page if applicable
    if request.user.is_authenticated:
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        else:
            return redirect("news:home")
    form = RegisterForm()
    # Attempt registration on POST request
    if request.method == "POST":
        form = RegisterForm(request.POST)
        # If the form is valid, create new user and on success login
        # the user. Redirect to the homepage or the previous page
        # if applicable
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            else:
                return redirect("news:home")
        # If the form is invalid, add error message
        messages.error(
            request, "Registration failed. Please put it valid information."
        )
    # Send empty form on GET request and form with errors if
    # registration failed
    return render(
        request, template_name="register.html", context={"register_form": form}
    )


def logout_request(request):
    """
    Logout Function Based View for logging out users.
    """
    logout(request)
    messages.info(request, f"You have been logged out. See you soon!")
    return redirect("news:home")
