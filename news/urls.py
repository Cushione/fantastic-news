from . import views
from django.urls import path

app_name = 'news'

urlpatterns = [
    path('', views.Home, name='home'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
]