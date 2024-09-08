from django import forms 
from recycle.models import RecycleRequest

class LoggedUserRecycleRequestForm(forms.ModelForm):
    class Meta:
        model = RecycleRequest
        fields = ('title', 'full_address', 'recycle_items')
        widgets = {
            'recycle_items':forms.Textarea(attrs={'rows':3, 'placeholder':'please give detail description about the times you want to recycle'}),
            'full_address':forms.Textarea(attrs={'rows':3, 'placeholder':'please enter your full address including flat/house, block/street, city and state'}),
            'title': forms.TextInput(attrs={'placeholder':'please enter the title'}),
        }

class GuestUserRecycleRequestForm(forms.ModelForm):
    class Meta:
        model = RecycleRequest
        fields = ('title','first_name', 'last_name', 'email', 'contact', 'full_address', 'recycle_items')
        widgets = {
            'recycle_items': forms.Textarea(attrs={'rows': 3, 'placeholder':'Please give detail description about the items you want to recycle.'}),
            'full_address': forms.Textarea(attrs={'rows': 3, 'placeholder':'Please enter your full address including flat/home, block/street, city and state.'}),
            'contact': forms.TextInput(attrs={'placeholder':'Please enter your contact number.'}),
            'email' : forms.TextInput(attrs={'placeholder':'Please enter your email address.','type':'email'}),
            'first_name' : forms.TextInput(attrs={'placeholder':'Please enter your first name.'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'Please enter your last name.'}),
            'title' : forms.TextInput(attrs={'placeholder':'Please enter the title.'})
        }
