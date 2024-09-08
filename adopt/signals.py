from django.db.models.signals import pre_save
from django.dispatch import receiver 
from adopt.models import Pet, PetBreed
from django.utils.text import slugify

@receiver(pre_save, sender=Pet)
def create_pet_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name) #Event.slug = Slugify(Event.title)

@receiver(pre_save, sender=PetBreed)
def create_pet_breed_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name) #Event.slug = Slugify(Event.title)