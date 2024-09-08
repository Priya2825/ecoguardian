from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Volunteer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='male')
    dob_month = models.IntegerField()
    dob_day = models.IntegerField()
    dob_year = models.IntegerField()
    phone = models.CharField(max_length=10)
    full_address = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    joined_on = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Sponser(models.Model):
    sponser = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=8)

    def __str__(self):
        return self.sponser


class Event(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=700, unique=True, blank= True, null= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    banner = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    description = models.TextField()
    venue = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(False)
    is_active = models.BooleanField(True)
    is_volunteer_required = models.BooleanField(False)
    volunteers = models.ManyToManyField(Volunteer, related_name='events')
    volunteers_capacity = models.IntegerField()
    sponsers = models.ManyToManyField(Sponser, related_name='events')
    terms = models.TextField()

    def __str__(self):
        return self.title

class Donation(models.Model):
    donated_name = models.CharField(max_length=200)
    amount = models.FloatField()
    donated_on = models.DateTimeField(auto_now_add=True)
    if_donated_for_event = models.BooleanField(default = False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.donated_name} donated {self.amount}"


class Sponsership(models.Model):
    LEVEL_CHOICES = [
        ('gold','Gold'),
        ('silver','Silver'),
        ('bronze', 'Bronze')
    ]
    sponser = models.ForeignKey(Sponser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete= models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.sponser.sponser} sponserd {self.event.title}"