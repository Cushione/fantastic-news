from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages

def register_request(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("news:home")
        messages.error(request, "Registration failed. Please put it valid information.")
    return render(request, template_name="register.html", context={"register_form":form})

def logout_request(request):
    logout(request)
    return redirect("news:home")