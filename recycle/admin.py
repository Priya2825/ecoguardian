from django.contrib import admin
from recycle.models import RecycleRequest, RecycleRequestStatus

# Register your models here.
admin.site.register(RecycleRequest)
admin.site.register(RecycleRequestStatus)