from django.contrib import admin
from .models import Article, Comment
from django_summernote.admin import SummernoteModelAdmin
from datetime import datetime
from django.contrib.auth import get_permission_codename


@admin.action(description="Publish selected articles", permissions=["publish"])
def publish_articles(self, request, queryset):
    """
    Custom admin action for publishing articles.
    Requires the permission publish.
    """
    queryset.update(status=1, published_on=datetime.now())


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    """
    Register the Article model in the Admin area.
    """

    list_display = (
        "title",
        "slug",
        "location",
        "status",
        "published_on",
        "number_of_likes",
    )
    search_fields = ["title", "content", "location"]
    list_filter = ("status", "type", "published_on", "location")
    date_hierarchy = "published_on"
    exclude = ("likes",)
    readonly_fields = ("status", "published_on", "number_of_likes")
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = "content"
    actions = [publish_articles]

    def has_publish_permission(self, request):
        """
        Checks if the user has the 'publish' permission.
        https://docs.djangoproject.com/en/4.1/ref/contrib/admin/actions/#setting-permissions-for-actions
        """
        return request.user.has_perm("%s.publish" % (self.opts.app_label))

    def has_change_permission(self, request, obj=None):
        """
        Overwrite default 'change' permission.
        If the article is still a draft, users with only the 'edit' permission
        can change the article.
        """
        if obj is not None and obj.status == 0:
            return request.user.has_perm("%s.edit" % (self.opts.app_label))
        return super().has_change_permission(request, obj=obj)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Register the Comment model in the Admin area.
    """

    list_display = ("__str__", "author", "article", "created_on")
    list_filter = ("created_on",)
    search_fields = ("content",)
    date_hierarchy = "created_on"
    readonly_fields = ("article", "author", "content")
