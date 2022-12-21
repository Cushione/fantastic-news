from django.shortcuts import render
from django.views import generic
from .models import Article

def Home(request):
	queryset = Article.objects.filter(status=1)
	latest_article = queryset.latest('published_on')
	main_article_list = queryset.exclude(id=latest_article.id)
	return render(
		request, 
		template_name="home.html", 
		context={
			'latest_article': latest_article,
			'main_article_list': main_article_list
			}
		)
