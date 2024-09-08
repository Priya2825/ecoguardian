from django.contrib import admin
from blog.models import Blog, Subscriber, Comment
# Register your models here.

admin.site.register(Blog)
admin.site.register(Subscriber)
admin.site.register(Comment)

