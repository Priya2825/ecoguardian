from django import forms
from django.contrib.auth.models import User
from organizers.models import Volunteer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['gender',
                'dob_day',
                'dob_month',
                'dob_year',
                'phone',
                'full_address',
                'profile_pic'
                ]
        widgets = {
            'dob_month': forms.NumberInput(attrs={'min':1,'max':12}),
            'dob_day': forms.NumberInput(attrs={'min':1,'max':31}),
            'dob_year': forms.NumberInput(attrs={'min':1900,'max':2024}),
            'phone': forms.TextInput(attrs={'maxlength':9}),
        }
class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    