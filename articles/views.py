from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
from articles import forms

from articles.models import Article
from rest_framework.response import Response


def article_list(request):
    articles = Article.objects.all().order_by('date')

    return render(request, 'articles/article_list.html', {'articles': articles})


def article_details(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})


@login_required(login_url="/accounts/login/")
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form':form})

@login_required(login_url="/accounts/login/")
def article_delete(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form':form})

def news_list(request):
    url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=2cdc982f0a5449649aa30f7e023875d1')
    response = requests.get(url)
    print(response.json()['articles'][0])
    return render(request, 'articles/news_list.html', {'news_list': response.json()['articles']})

def news_detail(request, pk):
    url = ('http://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=2cdc982f0a5449649aa30f7e023875d1')
    response = requests.get(url)
    return render(request, 'articles/news_detail.html', {'news': response.json()['articles'][pk]})