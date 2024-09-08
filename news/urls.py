from django.urls import path
from news.views import list_news, detail_news, delete_news, edit_news, create_news

urlpatterns = [
    path('list-news/', list_news, name='list-news'),
    path('create_news/', create_news, name='create-news'),
    path('detail_news/<slug:slug>/', detail_news, name='detail-news'),
    path('edit_news/<str:news_slug>/', edit_news, name='edit-news'), 
    path('delete_news/<str:news_slug>/', delete_news, name='delete-news'), 
]