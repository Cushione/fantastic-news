from django.shortcuts import render
from django.views import generic

def Home(request): 
	return render(request, template_name="home.html")
