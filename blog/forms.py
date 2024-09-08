from django import forms 
from blog.models import Blog, Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog 
        fields = ['title', 'author', 'body']
        widgets = {
            'body' : SummernoteWidget(), # or use summernoteinplacewidget

        }

class LoggedUserCommentForm(forms.ModelForm):
    class Meta: 
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={'rows':3, 'placeholder':"Add your comment..."}),
        }

class GuestUserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'body']
        widgets = {
            'body' : forms.Textarea(attrs={'rows':3, 'placeholder':"Add your comment...", 'required':True}),
            'email' : forms.EmailInput(attrs={'placeholder':"Enter your email address...", 'required':True}),
            'full_name' : forms.TextInput(attrs={'placeholder':"Add your full name..."}),

        }
