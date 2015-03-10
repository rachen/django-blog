from django.forms import ModelForm, CharField
from djblog.testblog.models import Article, Comment

class PartialArticleForm(ModelForm):
    class Meta:
        model = Article
        exclude = ('created', 'author')

class PartialCommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('created', 'article')
