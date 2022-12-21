from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'location', 'status', 'created_on')
    list_editable = ('status',)
    search_fields = ['title', 'content', 'location']
    list_filter = ('status', 'created_on', 'location')
    date_hierarchy = 'created_on'
    exclude = ('likes',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'article', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('content',)
    date_hierarchy = 'created_on'
    readonly_fields = ('article', 'author', 'content')
