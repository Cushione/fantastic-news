from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

app_name = 'news'

urlpatterns = [
    path('', views.Home, name='home'),
    path('comment/<slug:slug>', login_required(views.AddArticleComment.as_view(), login_url="/login"), name='add_article_comment'),
    path('like/<slug:slug>', login_required(views.ArticleLike.as_view(), login_url="/login"), name='article_like'),
    path('comments/<int:comment_id>', login_required(views.ArticleComments.as_view(), login_url="/login"), name='article_comments'),
    path('search-results/', views.SearchResults.as_view(), name='search-results'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
]