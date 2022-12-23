from . import views
from django.urls import path

app_name = 'news'

urlpatterns = [
    path('', views.Home, name='home'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('like/<slug:slug>', views.ArticleLike.as_view(), name='article_like'),
    path('comments/<int:comment_id>', views.ArticleComments.as_view(), name='article_comments'),
]