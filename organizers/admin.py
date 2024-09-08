from django.contrib import admin
from organizers.models import (Category, Volunteer, Event, Sponser, Sponsership, Donation)

# Register your models here.
admin.site.register(Category)
admin.site.register(Volunteer)
admin.site.register(Event)
admin.site.register(Sponser)
admin.site.register(Sponsership)
admin.site.register(Donation)