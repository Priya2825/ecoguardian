from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from organizers.models import Category, Event, Sponser, Donation, Volunteer
from organizers.forms import EventForm, DonationForm, EventDonationForm
from datetime import datetime
from urllib.parse import urlencode
from organizers.views import create_google_calendar_url
from unittest.mock import patch

# Create your tests here.

class CreateEventTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.volunteer = Volunteer.objects.create(user = self.user, dob_month=4, dob_day=1, dob_year=2021, phone='81234567', full_address='test_address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email='sponser@gmail.com', contact='91234567')

        self.valid_data={
            'title': 'This is test case',
            'category': self.category.id,
            'date_from': '2024-08-21',
            'date_to': '2024-08-24',
            'time_from': '10:00:00',
            'time_to': '09:00:00',
            'description':'This is test event description',
            'venue': 'singapore',
            'is_expired':False,
            'is_active':True,
            'is_volunteer_required':False,
            'volunteers':{self.volunteer.id},
            'sponsers': {self.sponser.id},
            'volunteers_capacity': 1,
            'terms': 'This is test terms'
        }
    
    def test_create_event_with_valid_data(self):
        response = self.client.post(reverse('create_events'), data=self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('all-events'))
        self.assertTrue(Event.objects.filter(title='This is test case').exists())

    def test_create_event_with_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        invalid_data['date_from'] = ''
        response = self.client.post(reverse('create_events'), data=invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        #self.assertTrue(Event.objects.filter(title='This is test event').exists())
        self.assertRedirects(response, reverse('create_events'))
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages),0)
        self.assertEqual(str(messages[0]), 'Error creating event. Please try again!')

class EditEventTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.volunteer = Volunteer.objects.create(user = self.user, dob_month=4, dob_day=1, dob_year=2021, phone='81234567', full_address='test_address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email='sponser@gmail.com', contact='91234567')

        self.event=Event.objects.create(
            title = 'This is test case',
            category = self.category,
            date_from = '2024-08-21',
            date_to = '2024-08-24',
            time_from = '10:00:00',
            time_to = '09:00:00',
            description = 'This is test event description',
            venue = 'singapore',
            is_expired = False,
            is_active = True,
            is_volunteer_required = False,
            volunteers_capacity = 1,
            terms = 'This is test terms'
        )
        self.valid_data={
            'title': 'This is test case 2',
            'category': self.category.id,
            'date_from': '2024-08-21',
            'date_to': '2024-08-24',
            'time_from': '10:00:00',
            'time_to': '09:00:00',
            'description':'This is updated test event description',
            'venue': 'singapore',
            'is_expired':False,
            'is_active':True,
            'is_volunteer_required':False,
            'volunteers':{self.volunteer.id},
            'sponsers': {self.sponser.id},
            'volunteers_capacity': 1,
            'terms': 'This is test terms'
        }
    
    def test_edit_event_get_request(self):
        self.event.volunteers.set([self.volunteer])
        self.event.sponsers.set([self.sponser])

        print(self.event.id,">>>>id")
        response = self.client.get(reverse('edit_events', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizers/edit_event.html')

        #check the form whether getting the data or not 
        form = response.context['form']
        self.assertIsInstance(form, EventForm)
        self.assertEqual(form.instance, self.event)
        self.assertEqual(form.initial['title'], self.event.title)

        self.assertIn(self.volunteer, form.instance.volunteers.all())
        self.assertIn(self.sponser, form.instance.sponsers.all())

    def test_edit_event_with_valid_data(self):
        response = self.client.post(reverse('edit_events', args=[self.event.id]), data=self.valid_data, follow=True)
        #self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('all-events'))
        self.event.refresh_from_db()
        self.assertTrue(self.event.title, 'This is test case 2')
        self.assertTrue(self.event.description, 'This is updated test event description')

    def test_edit_event_with_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        invalid_data['description'] = ''
        response = self.client.post(reverse('edit_events',args=[self.event.id]), data=invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        #self.assertTrue(Event.objects.filter(title='This is test event').exists())
        self.assertRedirects(response, reverse('edit_events', args=[self.event.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages),0)
        self.assertEqual(str(messages[0]), 'Error updating event. Please try again!')


class DeleteEventTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.volunteer = Volunteer.objects.create(user = self.user, dob_month=4, dob_day=1, dob_year=2021, phone='81234567', full_address='test_address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email='sponser@gmail.com', contact='91234567')

        self.event=Event.objects.create(
            title = 'This is test case',
            category = self.category,
            date_from = '2024-08-21',
            date_to = '2024-08-24',
            time_from = '10:00:00',
            time_to = '09:00:00',
            description = 'This is test event description',
            venue = 'singapore',
            is_expired = False,
            is_active = True,
            is_volunteer_required = False,
            volunteers_capacity = 1,
            terms = 'This is test terms'
        )
        
    def test_delete_event(self):
        self.assertTrue(Event.objects.filter(id=self.event.id).exists)
        response = self.client.post(reverse('delete_events', args=[self.event.id]), follow=True)
        self.assertFalse(Event.objects.filter(title='This is test case'). exists())
        self.assertRedirects(response, reverse('all-events'))

class DetailEventTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.volunteer = Volunteer.objects.create(user = self.user, dob_month=4, dob_day=1, dob_year=2021, phone='81234567', full_address='test_address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email='sponser@gmail.com', contact='91234567')

        self.event=Event.objects.create(
            title = 'This is test case',
            category = self.category,
            date_from = '2024-08-21',
            date_to = '2024-08-24',
            time_from = '10:00:00',
            time_to = '09:00:00',
            description = 'This is test event description',
            banner= 'image.jpg',
            venue = 'singapore',
            is_expired = False,
            is_active = True,
            is_volunteer_required = False,
            volunteers_capacity = 1,
            terms = 'This is test terms'
        )

    def test_detail_event(self):
        print(self.event.slug,">>>>>>slug")
        response = self.client.get(reverse('event_details', args=[self.event.slug]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizers/event_detail.html')
        self.assertEqual(response.context['event_detail'], self.event)

        combine_start_date_time = datetime.strptime(f'{self.event.date_from} {self.event.time_from}', '%Y-%m-%d %H:%M:%S')
        combine_end_date_time = datetime.strptime(f'{self.event.date_to} {self.event.time_to}', '%Y-%m-%d %H:%M:%S')
        
        # format the datetime obj
        start_formatted_dattime = combine_start_date_time.strftime('%Y%m%dT%H%M%S')
        end_formatted_dattime = combine_end_date_time.strftime('%Y%m%dT%H%M%S')

        params = {
        'action':'TEMPLATE',
        'text':self.event.title,
        'dates':f'{start_formatted_dattime}/{end_formatted_dattime}',
        'details': self.event.description,
        'location': self.event.venue,
        'trp':'false',
        'sprop':''
        }
        expected_google_calender_url = f'https://calendar.google.com/calendar/render?{urlencode(params)}'
        self.assertEqual(response.context['google_calender_url'], expected_google_calender_url)

class ListAllEventsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.volunteer = Volunteer.objects.create(user = self.user, dob_month=4, dob_day=1, dob_year=2021, phone='81234567', full_address='test_address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email='sponser@gmail.com', contact='91234567')

        self.event1=Event.objects.create(
            title = 'This is test case',
            category = self.category,
            date_from = '2024-08-21',
            date_to = '2024-08-24',
            time_from = '10:00:00',
            time_to = '09:00:00',
            description = 'This is test event description',
            banner= 'image.jpg',
            venue = 'singapore',
            is_expired = False,
            is_active = True,
            is_volunteer_required = False,
            volunteers_capacity = 1,
            terms = 'This is test terms'
        )
        self.event2=Event.objects.create(
            title = 'This is test case 2',
            category = self.category,
            date_from = '2024-08-21',
            date_to = '2024-08-24',
            time_from = '10:00:00',
            time_to = '09:00:00',
            description = 'This is test event description 2',
            banner= 'image.jpg',
            venue = 'singapore',
            is_expired = False,
            is_active = True,
            is_volunteer_required = False,
            volunteers_capacity = 1,
            terms = 'This is test terms'
        )
    @patch('organizers.views.create_google_calendar_url')
    def test_all_events(self, mock_create_google_calander_url):
        mock_create_google_calander_url.side_effect = lambda event: f'https://calendar.google.com/calendar/render?action=TEMPLATE&text={event.title}&dates={event.date_from}T{event.time_from}&details={event.description}&location={event.venue}&trp=false&sprop='
        
        response = self.client.get(reverse('all-events'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizers/all_events.html')
        self.assertEqual(len(response.context['all_events']), 2)
        
        # check the event and google calander url for the event1 
        event1, google_calander_url1, is_future_event1  = response.context['all_events'][0]
        self.assertEqual(event1, self.event1)
        self.assertEqual(google_calander_url1, mock_create_google_calander_url(self.event1))
        self.assertFalse(is_future_event1)
        
        # check the event and google calander url for the event1 
        event2, google_calander_url2, is_future_event2  = response.context['all_events'][1]
        self.assertEqual(event2, self.event2)
        self.assertEqual(google_calander_url2, mock_create_google_calander_url(self.event2))
        self.assertFalse(is_future_event2)

class DonationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000')
        self.client.login(username='admin', password='admin@000')
        self.category = Category.objects.create(name='animal rescue')
        self.volunteer = Volunteer.objects.create(user = self.user, dob_month=4, dob_day=1, dob_year=2021, phone='81234567', full_address='test_address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email='sponser@gmail.com', contact='91234567')

        self.event=Event.objects.create(
            title = 'This is test case',
            category = self.category,
            date_from = '2024-08-21',
            date_to = '2024-08-24',
            time_from = '10:00:00',
            time_to = '09:00:00',
            description = 'This is test event description',
            banner= 'image.jpg',
            venue = 'singapore',
            is_expired = False,
            is_active = True,
            is_volunteer_required = False,
            volunteers_capacity = 1,
            terms = 'This is test terms'
        )
    
    def test_donation_get_request(self):
        response = self.client.get(reverse('donation'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donation/donate.html')
        self.assertIn('get_all_donors', response.context)
        self.assertIn('total_general_donation', response.context)
        self.assertIn('events', response.context)
        self.assertIn('total_event_donation', response.context)
        self.assertIn('fund_raising_events', response.context)

    def test_donation_post_request(self):
        data = {
            'inputDonorName': 'user1',
            'inputAmount': 20.00
        }
        response = self.client.post(reverse('donation'), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('donation'))
        self.assertTrue(Donation.objects.filter(donated_name='user1', amount=20.00, if_donated_for_event=False).exists())

class DonateToEventTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@000', first_name='admin', last_name='user')
        self.client.login(username='admin', password='admin@000')
        
        self.category = Category.objects.create(name='test category')
        self.volunteer = Volunteer.objects.create(user=self.user, dob_month=4, dob_day=1, dob_year=2024, phone='545454545', full_address='test address')
        self.sponser = Sponser.objects.create(sponser='Test sponser', email="sponser@gmail.com", contact='54545454')
        
        self.event=Event.objects.create(
            title='This is test event',
            category=self.category,
            date_from= '2024-08-08',
            date_to= '2024-08-24',
            time_from= '10:00:00',
            time_to= '18:00:00',
            description= 'This is test event description',
            banner='image.jpg',
            venue= 'Bhilai',
            is_expired=False,
            is_active=True,
            is_volunteer_required=True,
            volunteers_capacity=1,
            terms='This is test terms'
        )
    
    def test_donation_to_event_get_request(self):
        response = self.client.get(reverse('donation_to_event', args=[self.event.slug]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donation/donate_to_event.html')
        self.assertIn('event', response.context)
        self.assertEqual(response.context['event'], self.event)
        
        
    def test_donation_to_event_post_request_authenticate(self):
        data = {
            'inputAmountEvent':100.05
        }
        full_name = self.user.first_name + ' ' + self.user.last_name
        response = self.client.post(reverse('donation_to_event', args=[self.event.slug]), data=data, follow=True)
        self.assertRedirects(response, reverse('donation'))
        self.assertTrue(Donation.objects.filter(donated_name=full_name, amount=100.05, if_donated_for_event=True, event=self.event).exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), 'Thank you for donating to this event')

    # def test_donation_to_event_post_request_unauthenticate(self):
    #     data = {
    #         'inputAmountEvent':110.05
    #     }
    #     response = self.client.post(reverse('donation_to_event', args=[self.event.slug]), data=data, follow=True)
    #     self.assertRedirects(response, reverse('donation'))
    #     self.assertFalse(Donation.objects.filter(amount=110.05).exists())
        
    #     messages = list(get_messages(response.wsgi_request))
    #     self.assertGreater(len(messages), 0)
    #     self.assertEqual(str(messages[0]), 'Please login to donate to this event')