from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from volunteer.forms import UserForm, VolunteerForm, UserLoginForm
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from organizers.models import Volunteer
from django.contrib.auth import get_user_model


class LoginUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        
    def test_login_user_valid_credentials(self):
        data = {
            'username': 'admin',
            'password': 'admin@000'
        }
        response = self.client.post(reverse('login-user'), data=data, follow=True)
        user = authenticate(username='admin', password='admin@000')
        self.assertTrue(user)
        self.assertRedirects(response, reverse('home'))
        
    def test_login_user_invalid_credentials(self):
        data = {
            'username': 'abc',
            'password': 'abc@0000'
        }
        response = self.client.post(reverse('login-user'), data=data, follow=True)
        user = authenticate(username='abc', password='abc@000')
        self.assertFalse(user)
        
    def test_login_user_get_request(self):
        response = self.client.get(reverse('login-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')
        self.assertIn('user_form', response.context)
        

        
class RegisterUserTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'first_name': 'test',
            'last_name': 'user',
            'password': 'test@000'
        }
        self.volunteer_data = {
            'gender':'male',
            'dob_day':5,
            'dob_month':5,
            'dob_year':2000,
            'phone':'4545454',
            'full_address':'test address',
            'profile_pic':'image.jpg'
        }
        
    def test_register_user_valid_data(self):
        data = {**self.user_data, **self.volunteer_data}
        response = self.client.post(reverse('register-user'), data=data, follow=True)
        
        # check user created
        user = User.objects.get(username='testuser')
        self.assertTrue(user)
        
        # check volunteer created
        volunteer = Volunteer.objects.get(user=user)
        self.assertEqual(volunteer.phone, '4545454')
        
        self.assertRedirects(response, reverse('login-user'))
        
    
    def test_register_user_invalid_data(self):
        invalid_data = {**self.user_data, 'username':''} # passing username empty means it's invalid
        data = {**invalid_data, **self.volunteer_data}
        
        response = self.client.post(reverse('register-user'), data = data, follow=True)
        self.assertFalse(User.objects.filter(email='test@gmail.com').exists())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_user.html')
        
        
    def test_register_user_get_request(self):
        response = self.client.get(reverse('register-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_user.html')
        self.assertIn('user_form', response.context)
        self.assertIn('volunteer_form', response.context)
        
        

class DeleteUserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@gmail.com', password='test@000')
        self.client.login(username='testuser', password='test@000')
        
    def test_logout_user(self):
        # first check if user is logged in or not
        response = self.client.get(reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        # now logout the user
        response = self.client.get(reverse('logout_user'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
        self.assertRedirects(response, reverse('home'))