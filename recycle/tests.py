from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from recycle.models import RecycleRequest, RecycleRequestStatus
from recycle.forms import LoggedUserRecycleRequestForm, GuestUserRecycleRequestForm
from django.contrib.messages import get_messages
from django.core import mail


class RecycleRequestTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        
        
    def test_recycle_request_create_authenticated(self):
        self.recycle1 = {
            'id': 1,
            'user':self.user,
            'title':'recycle test title',
            'first_name':'',
            'last_name' : '',
            'email': '',
            'contact':'',
            'full_address':'address1',
            'recycle_items':'paper, plastic'}
        response = self.client.post(reverse('create-recycle-request'), data=self.recycle1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('create-recycle-request'))
        self.assertEqual(RecycleRequest.objects.count(),1)
        self.assertTrue(RecycleRequest.objects.filter(user=self.user).exists())
        

class RecycleRequestViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        
        self.guest_user_data = {
            'title':'recycle glass',
            'first_name':'test',
            'last_name' : 'user',
            'email': 'test@gmail.com',
            'contact':'4545454',
            'full_address':'address2',
            'recycle_items':'glass1, glass2'
        }
        self.logged_user_data = self.guest_user_data.copy()
        self.logged_user_data.update({
            'user':self.user,
            'title': 'recycle metal'
        })
        
    def test_create_recycle_request_authenticated_user_post(self):
        response = self.client.post(reverse('create-recycle-request'), data=self.logged_user_data, follow=True)
        self.assertRedirects(response, reverse('create-recycle-request'))
        self.assertTrue(RecycleRequest.objects.filter(title='recycle metal').exists())
        self.assertEqual(RecycleRequest.objects.get(title='recycle metal').user, self.user)
        
        
    def test_create_recycle_request_guest_user_post(self):
        response = self.client.post(reverse('create-recycle-request'), data=self.guest_user_data, follow=True)
        self.assertRedirects(response, reverse('create-recycle-request'))
        self.assertTrue(RecycleRequest.objects.filter(title='recycle glass').exists())
        self.assertFalse(RecycleRequest.objects.get(title='recycle glass').user == '')
        


class RecycleRequestListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.recycle_request1 = RecycleRequest.objects.create(
            user=self.user,
            title='recycle paper',
            full_address='address1',
            recycle_items='paper'
        )
        self.recycle_request2 = RecycleRequest.objects.create(
            user=self.user,
            title='recycle plastic',
            full_address='address1',
            recycle_items='plastic'
        )
        self.status1 = RecycleRequestStatus.objects.create(
            request=self.recycle_request1
        )
        self.status2 = RecycleRequestStatus.objects.create(
            request=self.recycle_request2
        )

    def test_recycle_request_list_view(self):
        response = self.client.get(reverse('recycle-request-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recycle_list.html')
        all_recycle_requests = response.context['all_recycle_requests']
        self.assertEqual(all_recycle_requests.count(), 2)
        self.assertEqual(all_recycle_requests[0].request.title, 'recycle plastic')
        self.assertEqual(all_recycle_requests[1].request.title, 'recycle paper')
        
        
    def test_recycle_request_empty(self):
        RecycleRequest.objects.all().delete()
        response = self.client.get(reverse('recycle-request-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_recycle_requests']), 0)
        
