from django import forms 
from news.models import News 
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class NewsForm(forms.ModelForm):
    class Meta:
        model = News 
        fields = ['title', 'category', 'author', 'body']
        widgets = {
            'body' : SummernoteWidget(), # or use summernoteinplacewidget

        }