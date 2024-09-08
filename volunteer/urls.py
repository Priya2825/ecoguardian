from django.urls import path
from volunteer.views import login_user,register_user, logout_user

urlpatterns = [
    path('login_user/', login_user, name='login-user'),
    path('register_user/', register_user, name='register-user'),
    path('logout-user/', logout_user, name='logout_user'),
]