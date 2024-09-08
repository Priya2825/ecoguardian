from django.db.models.signals import pre_save
from django.dispatch import receiver 
from recycle.models import RecycleRequest
from django.utils.text import slugify

@receiver(pre_save, sender=RecycleRequest)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title) #Event.slug = Slugify(Event.title)