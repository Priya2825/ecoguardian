from django.urls import path
from organizers.views import home, event_details, all_events, create_event, edit_event, delete_event, donation, donation_to_event

urlpatterns = [
    path('', home, name='home'),
    path('event/<str:event_slug>/', event_details, name='event_details'),
    path('all-events/', all_events, name='all-events'),
    path('create-event/', create_event, name='create_events'),
    path('edit-event/<int:event_id>/', edit_event, name='edit_events'),
    path('delete-event/<int:event_id>/', delete_event, name='delete_events'),
    
    #donation urls
    path('donation/', donation, name='donation'),
    path('donation-to-event/<str:event_slug>/', donation_to_event, name='donation_to_event'),
]