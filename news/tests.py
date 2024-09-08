from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from news.forms import NewsForm
from django.contrib.messages import get_messages
from news.models import Category, News


class NewsCreatTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.valid_data={
            'title':'This is test news',
            'category':self.category.id,
            'body': 'This is test news description',
            'author':self.user.id
        }
        
    def test_create_news_with_valid_data(self):
        response = self.client.post(reverse('create-news'), self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(News.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), 'News created successfully')
        self.assertRedirects(response, reverse('list-news'))
        
    def test_create_news_with_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        response = self.client.post(reverse('create-news'), invalid_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), 'Error creating news')
        self.assertRedirects(response, reverse('create-news'))
        
        
class NewsListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.news = News.objects.create(title='This is test news', category=self.category, body='This is test news description', author=self.user)
        
    def test_list_news_view(self):
        response = self.client.get(reverse('list-news'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        self.assertTemplateUsed(response, 'list_news.html')
    
    
class NewsDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.news = News.objects.create(title='This is test news', category=self.category, body='This is test news description', author=self.user)

    def test_news_detail_view(self):
        response = self.client.get(reverse('detail-news', args=[self.news.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.news.title)
        self.assertContains(response, self.news.body)
        self.assertTemplateUsed(response, 'detail_news.html')
        
        
class NewsEditTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.news = News.objects.create(title='This is test news', category=self.category, body='This is test news description', author=self.user)
        self.valid_data={
            'title':'This is test news updated',
            'category':self.category.id,
            'body': 'This is test news description updated',
            'author':self.user.id
        }
        
    def test_edit_news_with_valid_data(self):
        response = self.client.post(reverse('edit-news', args=[self.news.slug]), self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(News.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), 'News updated successfully')
        self.assertRedirects(response, reverse('list-news'))
        
        
    def test_edit_news_with_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        response = self.client.post(reverse('edit-news', args=[self.news.slug]), data=invalid_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), 'Error updating news')
        self.assertRedirects(response, reverse('edit-news', args=[self.news.slug]))
        
        
class NewsDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.news = News.objects.create(title='This is test news', category=self.category, body='This is test news description', author=self.user)

    def test_delete_news(self):
        response = self.client.post(reverse('delete-news', args=[self.news.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(News.objects.count(), 0)
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), 'News deleted successfully')
        self.assertRedirects(response, reverse('list-news'))