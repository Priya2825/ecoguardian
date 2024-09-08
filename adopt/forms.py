from django import forms
from adopt.models import Pet, PetBreed, PetContact

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'
        exclude = ['slug', 'owner_name']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class AdoptionForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    contact = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea, help_text="Why do you want to adopt this pet?")

    class Meta:
        model = PetContact
        fields = ['first_name','last_name', 'email', 'contact', 'message']


class PetContactForm(forms.ModelForm):
    class Meta:
        model = PetContact
        fields = ['first_name', 'last_name', 'email', 'contact', 'message']
