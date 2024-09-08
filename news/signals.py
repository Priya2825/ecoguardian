from django.db.models.signals import pre_save
from django.dispatch import receiver 
from news.models import News, Category
from django.utils.text import slugify

@receiver(pre_save, sender=News)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title) #Event.slug = Slugify(Event.title)

@receiver(pre_save, sender=Category)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name) #Event.slug = Slugify(Event.title)