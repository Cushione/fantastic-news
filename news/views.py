from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from .models import Article, Comment
from .forms import CommentForm
from django.contrib import messages
from django.http import HttpResponse, QueryDict, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from functools import reduce
import operator
from django.db.models import Q


def Home(request):
	queryset = Article.objects.filter(status=1, type=0)
	if not queryset.exists():
		return HttpResponseServerError()
	latest_article = queryset.latest() 
	article_list = queryset.exclude(id=latest_article.id)
	paginator = Paginator(article_list, 4)
	page_number = request.GET.get('page')
	main_article_list = paginator.get_page(page_number)

	secondary_article_list = Article.objects.filter(status=1, type=1)[:5]

	return render(
		request, 
		template_name="home.html", 
		context={
			'latest_article': latest_article,
			'main_article_list': main_article_list,
			'secondary_article_list': secondary_article_list
			}
		)

class ArticleDetail(View):

	def get(self, request, slug, *args, **kwargs):
		queryset = Article.objects.filter(status=1)
		article = get_object_or_404(queryset, slug=slug)
		comments = article.comments.all()
		liked = False
		if article.likes.filter(id=request.user.id).exists():
			liked = True

		return render(
			request,
			"article_detail.html",
			{
				"article": article,
				"comments": comments,
				"liked": liked,
				"comment_form": CommentForm()
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


class ArticleComments(View):
	def delete(self, request, comment_id, *args, **kwargs):
		comment = get_object_or_404(Comment, id=comment_id)
		comment.deleted = True
		comment.save()
		return HttpResponse()
		
	def post(self, request, comment_id, *args, **kwargs):
		comment = get_object_or_404(Comment, id=comment_id)
		comment_form = CommentForm(data=request.POST)

		if comment_form.is_valid():
			comment.content = comment_form.cleaned_data.get('content')
			comment.save()
			return HttpResponse()
		return HttpResponseBadRequest()

class AddArticleComment(View):
	def post(self, request, slug, *args, **kwargs):
		queryset = Article.objects.filter(status=1)
		article = get_object_or_404(queryset, slug=slug)
	
		comment_form = CommentForm(data=request.POST)

		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.author = request.user
			comment.article = article
			comment.save()
		else:
			messages.error(request, "Invalid comment.")

		return redirect(reverse('news:article_detail', args=[slug]))


class SearchResults(View):
	def get(self, request, *args, **kwargs):
		keyword_list = request.GET.get('keywords', '')
		if keyword_list == '':
			return HttpResponseNotFound()
		keywords = keyword_list.split()
		query_title = reduce(
			operator.and_, 
			(Q(
				Q(title__icontains=x) |
				Q(location__icontains=x) |
				Q(content__icontains=x))
				for x in keywords))
		search_results = Article.objects.filter(query_title)
	
		paginator = Paginator(search_results, 10)
		page_number = request.GET.get('page')
		current_page = paginator.get_page(page_number)
		return render(
			request,
			"search-results.html",
			{
				"search_results": current_page,
				"keywords": keyword_list
				},
		)