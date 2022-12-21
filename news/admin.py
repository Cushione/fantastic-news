from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin
from datetime import datetime

@admin.action(description='Publish selected articles')
def publish_articles(self, request, queryset):
    queryset.update(status=1, published_on=datetime.now())

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'location', 'status', 'published_on', 'number_of_likes')
    search_fields = ['title', 'content', 'location']
    list_filter = ('status', 'created_on', 'location')
    date_hierarchy = 'created_on'
    exclude = ('likes',)
    readonly_fields = ('status', 'published_on', 'number_of_likes')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')
    actions = [publish_articles]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'article', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('content',)
    date_hierarchy = 'created_on'
    readonly_fields = ('article', 'author', 'content')
