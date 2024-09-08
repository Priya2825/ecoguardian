from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class PetBreed(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique = True, blank=True, null=True)
    description = models.TextField()
    size = models.IntegerField(default=0)
    lifespan = models.IntegerField(default=0)
    trainability = models.IntegerField(default=0)
    bark = models.IntegerField(default=0)
    energy = models.IntegerField(default=0)
    image = models.ImageField(upload_to='breed_images/{name}/', blank=True, null=True)

    def __str__(self):
        return self.name



class Pet(models.Model):
    SEX_CHOICE = (
        ("male", 'MALE'),
        ("female", 'FEMALE')
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique = True, blank=True, null=True)
    owner_name = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.ForeignKey(PetBreed, on_delete=models.CASCADE)
    sex = models.CharField(max_length=50)
    price = models.FloatField(default=0.00)
    location = models.CharField(max_length=500)
    contact = models.CharField(max_length=9)
    dob = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images/{name}/', blank=True, null=True)

    def __str__(self):
        return self.name


class PetContact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    email = models.EmailField()
    contact = models.CharField(max_length=9)
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AdoptionStatus(models.Model):
    adoptee = models.ForeignKey(PetContact, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    pet_adopt_request = models.BooleanField(default=False)
    adoption_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

