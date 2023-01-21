from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View
from .models import Article, Comment
from .forms import CommentForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from functools import reduce
import operator
from django.db.models import Q


def Home(request):
	"""
	Home Function Based View for displaying the homepage.
	"""
	# Find all the published main articles
	queryset = Article.objects.filter(status=1, type=0)
	if not queryset.exists():
		return HttpResponseServerError()
	# Get the latest article from the results
	latest_article = queryset.latest() 
	# Remove the latest article from the article list
	article_list = queryset.exclude(id=latest_article.id)

	# Paginate the article list
	paginator = Paginator(article_list, 4)
	page_number = request.GET.get('page')
	main_article_list = paginator.get_page(page_number)

	# Find the five latest published secondary articles
	secondary_article_list = Article.objects.filter(status=1, type=1)[:5]

	# Render the home view with the "home.html" template
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
	"""
	Article Detail Class Based View for displaying specific article.
	"""
	def get(self, request, slug, *args, **kwargs):
		# Find specified article or show error page if not found
		queryset = Article.objects.filter(status=1)
		article = get_object_or_404(queryset, slug=slug)
		# Load all the comments of the article
		comments = article.comments.all()
		# Check if the user liked the article
		liked = False
		if article.likes.filter(id=request.user.id).exists():
			liked = True

		# Render the article detail view with the "article-detail.html" template
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
	"""
	Article Like Class Based View for toggling likes.
	"""
	def post(self, request, slug, *args, **kwargs):
		# Find specified article or show error page if not found
		article = get_object_or_404(Article, slug=slug)

		# Toggle user like by adding or removing them from the list
		if article.likes.filter(id=request.user.id).exists():
			messages.info(request, "You have unliked this article.")
			article.likes.remove(request.user)
		else:
			article.likes.add(request.user)
			messages.success(request, "Thank you for giving this article a like!")

		# Redirect to the article detail view
		return redirect(reverse('news:article_detail', args=[slug]))


class ArticleComments(View):
	"""
	Article Comments Class Based View handling comment requests.
	"""
	def delete(self, request, comment_id, *args, **kwargs):
		# Find specified comment or show error page if not found
		comment = get_object_or_404(Comment, id=comment_id)
		# Only allow the owner of the comment to delete
		if comment.author == request.user:
			# Set deleted flag
			comment.deleted = True
			comment.save()
			# Return success response
			return HttpResponse()
		messages.error(request, "You are not allowed to delete this comment.")
		return HttpResponseForbidden()
		
	def post(self, request, comment_id, *args, **kwargs):
		# Find specified comment or show error page if not found
		comment = get_object_or_404(Comment, id=comment_id)
		comment_form = CommentForm(data=request.POST)
		# Only allow the owner of the comment to edit
		if comment.author == request.user:
			# Update the comment content if form is valid
			if comment_form.is_valid():
				comment.content = comment_form.cleaned_data.get('content')
				comment.save()
				# Return success response
				return HttpResponse()
			# If form is invalid, return bad request response
			return HttpResponseBadRequest()
		messages.error(request, "You are not allowed to delete this comment.")
		return HttpResponseForbidden()


class AddArticleComment(View):
	"""
	Add Article Comments Class Based View for adding comments.
	"""
	def post(self, request, slug, *args, **kwargs):
		# Find specified article or show error page if not found
		queryset = Article.objects.filter(status=1)
		article = get_object_or_404(queryset, slug=slug)
	
		comment_form = CommentForm(data=request.POST)
		# If comment form is valid, set article and author and save comment
		if comment_form.is_valid():
			comment = comment_form.save(commit=False)
			comment.author = request.user
			comment.article = article
			comment.save()
			messages.success(request, "Comment added successfully.")
		else:
			# If invalid, set error message
			messages.error(request, "Invalid comment.")
		# Redirect to the article detail view
		return redirect(reverse('news:article_detail', args=[slug]))


class SearchResults(View):
	"""
	SearchResults Class Based View for displaying search results.
	"""
	def get(self, request, *args, **kwargs):
		# Get keywords from the request
		keyword_list = request.GET.get('keywords', '')
		# Redirect to the homepage if no keywords are given
		if keyword_list == '':
			return redirect("news:home")
		# Split keywords into list
		keywords = keyword_list.split()
		# Create search query
		# Find any article that has all the keywords in either the title, location, or content
		search_query = reduce(
			operator.and_, 
			(Q(
				Q(title__icontains=x) |
				Q(location__icontains=x) |
				Q(content__icontains=x))
				for x in keywords))
		search_results = Article.objects.filter(search_query)
	
		# Paginate the search result
		paginator = Paginator(search_results, 10)
		page_number = request.GET.get('page')
		current_page = paginator.get_page(page_number)
		# Render the search results view with the "search-results.html" template
		return render(
			request,
			"search-results.html",
			{
				"search_results": current_page,
				"keywords": keyword_list
				},
		)