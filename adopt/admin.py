from django.contrib import admin
from adopt.models import PetBreed, Pet, PetContact, AdoptionStatus

# Register your models here.
admin.site.register(PetBreed)
admin.site.register(Pet)
admin.site.register(PetContact)
admin.site.register(AdoptionStatus)