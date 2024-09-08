from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique = True, blank=True, null=True)
    
    def __str__(self):
        return self.name 


class News(models.Model):
    title = models.CharField(max_length = 200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique = True, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    news_image = models.ImageField(upload_to='news_images/', blank=True, null=True)


    def __str__(self):
        return self.title
