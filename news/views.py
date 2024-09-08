from django.shortcuts import render, get_object_or_404, redirect
from news.models import News
from news.forms import NewsForm
from django.db.models import Q
from django.contrib import messages


def create_news(request):
    context = {}
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit= False)
            news.author = request.user
            news.save()
            messages.success(request, 'News created successfully')
            return redirect('list-news')
        else:
            messages.error(request, 'Error creating news')
            return redirect('create-news')
    else:
        form = NewsForm()
    context['form'] = form
    return render(request, 'create_news.html', context)

def list_news(request):
    context = {}
    query = request.GET.get('q', '')
    if query:
        all_news = News.objects.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query) | 
            Q(category__name__icontains=query) | 
            Q(author__first_name__icontains=query) | 
            Q(author__last_name__icontains=query)
        )
        context['all_news'] = all_news
    else:
        all_news = News.objects.all()
        context['all_news'] = all_news
    return render(request, 'list_news.html', context)


def detail_news(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'detail_news.html', {'news': news})

def delete_news(request, news_slug):
    news = get_object_or_404(News, slug=news_slug)
    news.delete()
    messages.success(request, 'News deleted successfully')
    return redirect('list-news')
    
def edit_news(request, news_slug):
    context = {}
    news = get_object_or_404(News, slug=news_slug)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit= False)
            news.author = request.user
            news.save()
            messages.success(request, 'News updated successfully')
            return redirect('list-news')
        else:
            messages.error(request, 'Error updating news')
            return redirect('edit-news', news_slug=news.slug)
    else:
        form = NewsForm(instance=news)
    context['form'] = form
    return render(request, 'edit_news.html', context)