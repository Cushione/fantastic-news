from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from .models import Article

def Home(request):
	queryset = Article.objects.filter(status=1)
	latest_article = queryset.latest('published_on')
	article_list = queryset.exclude(id=latest_article.id)
	paginator = Paginator(article_list, 4)
	page_number = request.GET.get('page')
	main_article_list = paginator.get_page(page_number)
	return render(
		request, 
		template_name="home.html", 
		context={
			'latest_article': latest_article,
			'main_article_list': main_article_list
			}
		)

class ArticleDetail(View):

	def get(self, request, slug, *args, **kwargs):
		queryset = Article.objects.filter(status=1)
		article = get_object_or_404(queryset, slug=slug)
		liked = False
		if article.likes.filter(id=request.user.id).exists():
			liked = True

		return render(
			request,
			"article_detail.html",
			{
				"article": article,
				"liked": liked
			},
		)

class ArticleLike(View):
	def post(self, request, slug, *args, **kwargs):
		article = get_object_or_404(Article, slug=slug)

		if article.likes.filter(id=request.user.id).exists():
			article.likes.remove(request.user)
		else:
			article.likes.add(request.user)

		return redirect(reverse('news:article_detail', args=[slug]))