from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class RecycleRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    full_address = models.TextField()
    recycle_items = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else self.first_name}"

class RecycleRequestStatus(models.Model):
    request = models.OneToOneField(RecycleRequest, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request.first_name} - {self.status}"