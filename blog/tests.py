from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import Blog, Subscriber, Comment 
from blog.forms import BlogForm
from django.contrib.messages import get_messages

# Create your tests here.

# class BlogTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='admin', password='admin@000')
#         self.client.login(username='admin', password='admin@000')

#     def test_blog_create_with_valid_data(self):
#         data = {
#             'title':'Test Blog',
#             'body': 'This is my test blog',
#             'author': self.user
#         }
#         response = self.client.post(reverse('create-blog'), data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Blog.objects.filter(title='Test Blog').exists())

