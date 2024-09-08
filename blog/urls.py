from django.urls import path
from blog.views import create_blog, list_blogs, detail_blog, edit_blog, delete_blog

urlpatterns = [
    path('create_blog/', create_blog, name='create-blog'),
    path('edit_blog/<str:blog_slug>/', edit_blog, name='edit-blog'), 
    path('delete_blog/<str:blog_slug>/', delete_blog, name='delete-blog'), 
    path('list_blogs/', list_blogs, name='list-blogs'),
    path('<str:blog_slug>/', detail_blog, name='detail-blog'),
]