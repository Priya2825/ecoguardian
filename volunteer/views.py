from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from volunteer.forms import UserForm, VolunteerForm, UserLoginForm
from organizers.models import Volunteer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_user(request):
    if request.method == "POST":
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username and password')
            return redirect('login-user')
    else: 
        user_form = UserLoginForm()
    return render(request,'login_user.html', {'user_form':user_form})

def register_user(request):
    """
    registering the user with UserForm details and additional volunteer details 
    """
    if request.method == "POST":
        user_form = UserForm(request.POST)
        volunteer_form = VolunteerForm(request.POST, request.FILES)
        if user_form.is_valid() and volunteer_form.is_valid():
            user = user_form.save(commit = False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            volunteer = volunteer_form.save(commit=False)
            volunteer.user = user
            volunteer.save()

            #redirect the user to login page after successful registeration
            return redirect('login-user')
    else:
        user_form = UserForm()
        volunteer_form = VolunteerForm()
    return render(request, 'register_user.html', {'user_form': user_form, 'volunteer_form': volunteer_form})



def logout_user(request):
    logout(request)
    return redirect('home')