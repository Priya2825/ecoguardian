from django.db.models.signals import pre_save
from django.dispatch import receiver 
from organizers.models import Event
from django.utils.text import slugify

@receiver(pre_save, sender=Event)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title) #Evet.slug = Slugify(Event.title)