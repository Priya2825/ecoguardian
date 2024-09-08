from django import forms 
from organizers.models import Event, Donation

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'date_from', 'time_from', 'date_to', 'time_to', 'banner', 'description', 'venue','is_expired','is_active', 'is_volunteer_required', 'volunteers', 'volunteers_capacity', 'sponsers', 'terms',]
        widgets = {
            'date_from': forms.DateInput(attrs={'type':'date'}),
            'date_to': forms.DateInput(attrs={'type':'date'}),
            'time_from': forms.DateInput(attrs={'type':'time'}),
            'time_to': forms.DateInput(attrs={'type':'time'})
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donated_name', 'amount']

class EventDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donated_name', 'amount', 'event']