from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_comment_count(self):
        return len(Comment.objects.filter(article=self))


class Comment(models.Model):
    article = models.ForeignKey(Article)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=80, blank=True)

