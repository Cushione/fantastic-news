from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Article Status Tuple
STATUS = ((0, "Draft"), (1, "Published"))
# Article Type Tuple
TYPE = ((0, "Main"), (1, "Secondary"))


class Article(models.Model):
    """
    Article Model
    """

    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="news_articles"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    location = models.CharField(max_length=200)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name="article_likes", blank=True
    )
    type = models.IntegerField(choices=TYPE, default=0)
    original_article = models.URLField(blank=True)

    class Meta:
        """
        Article Meta Data
        """

        # Order articles by published date in descending order
        ordering = ["-published_on"]
        # Get the latest article by published date
        get_latest_by = "published_on"
        # Custom permissions for articles
        permissions = [
            ("publish", "Can publish article"),
            ("edit", "Can edit article draft"),
        ]

    def __str__(self):
        """
        Returns the title of the article
        """
        return self.title

    def number_of_likes(self):
        """
        Returns the number of likes
        """
        return self.likes.count()

    def number_of_comments(self):
        """
        Returns the number of existing comments
        """
        return self.comments.filter(deleted=False).count()


class Comment(models.Model):
    """
    Comment Model
    """

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="article_comments"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.content[0:100]
