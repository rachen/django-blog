from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.utils import simplejson

from datetime import datetime

from testblog.forms import *


def index(request):
    # For the index
    articles = Articles.objects.all().order_by('-created')
    for article in articles:
        setattr(article, 'comment_count', article.get_comment_count())
    paginator = Paginator(articles, 2)

    # Pagination stuff
    # If invalid page aka letters
    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    # if number is too high, go to last page
    try:
        articles = paginator.page(page)
    except (InvalidPage, EmptyPage):
        articles = paginator.page(paginator.num_pages)

    return render_to_response("index.html", {'articles' : articles, 'user':request.user })


def login(request):
    next = request.GET['next'] if 'next' in request.GET else '/'

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth_login(request, user)
            # Redirect to a success page.
            return redirect('djblog.testblog.views.index')
        else:
            form = AuthenticationForm()
            form.errors.update(errors="Your username or password is incorrect")
            req_context = RequestContext(request, {"form": form, "next": next})
            return render_to_response("registration/login.html", context_instance=req_context)
    else:
        form = AuthenticationForm()
    req_context = RequestContext(request, {"form": form, "next": next})
    return render_to_response("registration/login.html", context_instance=req_context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            request.user = new_user
            return redirect("/")
    else:
        form = UserCreationForm()
    req_context = RequestContext(request, {"form": form})
    return render_to_response("registration/register.html", context_instance=req_context)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = PartialArticleForm(request.POST)
        if form.is_valid():
#            form.cleaned_data['author'] = request.user
            article = form.save(commit=False)
            article.author = request.user
            article.created = datetime.now()
            article.save()
            return redirect("/")
    else:
        form = PartialArticleForm()
    req_context = RequestContext(request, {'form': form, 'user': request.user})
    return render_to_response("add_edit_article.html", context_instance=req_context)


def get_article(request, article_id=None, slug=None):
    if article_id:
        article = Articles.objects.get(id=article_id)
    elif slug:
        article = Articles.objects.get(slug=slug)
    return render_to_response("article.html", {'article': article, 'user':request.user})


def get_article_by_slug(request, slug):
    article = Articles.objects.get(slug=slug)
    comments = Comments.objects.filter(article=article)
    comment_count = len(comments)
    user = request.user if request.user else ''
    form = PartialCommentForm(initial={'article':article, 'author':user})
    req_context = RequestContext(request, {'article': article, 'user':request.user, 'form':form, 'comments':comments, 'comment_count': comment_count})
    return render_to_response("article.html", context_instance=req_context)


def add_comment(request, slug):
    article = Articles.objects.get(slug=slug)
    if request.method == 'POST' and request.is_ajax():
        form = PartialCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article.id
            comment.save()
            output = "Comment: " + comment.body + " By: " + comment.author
            json = simplejson.dumps(output)
            return HttpResponse(json, mimetype='application/json')
    else:
        user = request.user if request.user else ''
        form = PartialCommentForm(initial={'article': article, 'author': user})
        req_context = RequestContext(request, {'article': article, 'user':request.user, 'form':form, 'comments':comments, 'comment_count': comment_count})
    return render_to_response("article.html", context_instance=req_context)


@login_required
def edit_article(request, article_id):
    article = Articles.objects.get(id=article_id)
    if request.user.id != article.author.id:
        return HttpResponseForbidden('Forbidden!')
    if request.method == 'POST':
        form = PartialArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return get_article(request, article.id)
            # Possibly update created time
    else:
        form = PartialArticleForm(instance=article)
    req_context = RequestContext(request, {'article':article, 'form':form, 'editing': True })
    return render_to_response("add_edit_article.html", context_instance=req_context)

@login_required
def delete_article(request, article_id):
    article = Articles.objects.get(id=article_id)
    if request.user.id != article.author.id:
        return HttpResponseForbidden('Forbidden!')
    else:
        article.delete()
    return redirect('/')
