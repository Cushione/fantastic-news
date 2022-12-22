from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_request(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect("news:home")
        messages.error(request, "Invalid username or password.")
    return render(request, template_name="login.html", context={"login_form":form})

def register_request(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect("news:home")
        messages.error(request, "Registration failed. Please put it valid information.")
    return render(request, template_name="register.html", context={"register_form":form})

def logout_request(request):
    logout(request)
    return redirect("news:home")