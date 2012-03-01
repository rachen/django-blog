from django.forms import ModelForm, CharField
from djblog.testblog.models import Articles, Comments

class PartialArticleForm(ModelForm):
    class Meta:
        model = Articles
        exclude = ('created', 'author')

class PartialCommentForm(ModelForm):
    class Meta:
        model = Comments
        exclude = ('created', 'article')