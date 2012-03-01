from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_comment_count(self):
        return len(Comments.objects.filter(article=self))


class Comments(models.Model):
    article = models.ForeignKey(Articles)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=80, blank=True)





