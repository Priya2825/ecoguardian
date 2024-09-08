from django.shortcuts import render, redirect, get_object_or_404
from organizers.models import Event, Donation
from organizers.forms import EventForm
from datetime import datetime
from urllib.parse import urlencode
from django.contrib import messages

# Create your views here.
def home(request):
    context = {}
    all_events = Event.objects.all()
    context['all_events'] = all_events
    return render(request, 'home.html', context)

def event_details(request, event_slug):
    context = {}
    event_detail = Event.objects.get(slug=event_slug)

    combine_start_date_time = datetime.strptime(f'{event_detail.date_from} {event_detail.time_from}', '%Y-%m-%d %H:%M:%S')
    combine_end_date_time = datetime.strptime(f'{event_detail.date_to} {event_detail.time_to}', '%Y-%m-%d %H:%M:%S')
    print(combine_start_date_time, '>>>>>>>>>combined start date time') #2024-06-22 23:45:00
    print(combine_end_date_time, '>>>>>>>>>combined end date time') #2024-06-22 23:45:00
    
    # format the datetime obj
    start_formatted_dattime = combine_start_date_time.strftime('%Y%m%dT%H%M%S')
    end_formatted_dattime = combine_end_date_time.strftime('%Y%m%dT%H%M%S')

    params = {
        'action':'TEMPLATE',
        'text':event_detail.title,
        'dates':f'{start_formatted_dattime}/{end_formatted_dattime}',
        'details': event_detail.description,
        'location': event_detail.venue,
        'trp':'false',
        'sprop':''
    }

    google_calender_url = f'https://calendar.google.com/calendar/render?{urlencode(params)}'
    context["event_detail"] = event_detail
    context['google_calender_url'] = google_calender_url
    return render(request, 'organizers/event_detail.html', context)

def all_events(request):
    context = {}
    all_events = Event.objects.all()
    event_links = [] # [(event1, calanderurl1), (event2, calenderurl2), (event3, calenderurl3)]
    
    for event in all_events:
        google_calander_url = create_google_calendar_url(event)
        #combine the date and time 
        event_date_time = datetime.combine(event.date_from, event.time_from)
        #check if the event date and time is in the past, future 
        is_future_event = event_date_time > datetime.now()
        print(is_future_event, ">>>>>printing if future event")
        event_links.append((event, google_calander_url, is_future_event))
    
    print(event_links,">>>>prepared event link")
    # o/p: [(<Event: Test Event one>, 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=Test+Event+one&dates=20240622T234500%2F20240524T235200&details=Test+Event&location=Begumpet+Hyderabad&trp=false&sprop=')]
    context['all_events'] = event_links
    
    return render(request, 'organizers/all_events.html', context)

# creating a function to prepare the google calander url
def create_google_calendar_url(event):
    # formate the datetime in this way '%Y%m%dT%H%M%S'
    combine_start_date_time = datetime.strptime(f'{event.date_from} {event.time_from}', '%Y-%m-%d %H:%M:%S')
    combine_end_date_time = datetime.strptime(f'{event.date_to} {event.time_to}', '%Y-%m-%d %H:%M:%S')
    print(combine_start_date_time, '>>>>>>>>>combined start date time') #2024-06-22 23:45:00
    print(combine_end_date_time, '>>>>>>>>>combined end date time') #2024-06-22 23:45:00
    
    # format the datetime obj
    start_formatted_dattime = combine_start_date_time.strftime('%Y%m%dT%H%M%S')
    end_formatted_dattime = combine_end_date_time.strftime('%Y%m%dT%H%M%S')
    
    params = {
        'action':'TEMPLATE',
        'text':event.title,
        'dates':f'{start_formatted_dattime}/{end_formatted_dattime}',
        'details': event.description,
        'location': event.venue,
        'trp':'false',
        'sprop':''
    }
    
    # https://calendar.google.com/calendar/render?action=TEMPLATE&text=TEST+EVENT=1
    # o/p: https://calendar.google.com/calendar/render?action=TEMPLATE&text=Test+Event+one&dates=20240622T234500%2F20240524T235200&details=Test+Event&location=Begumpet+Hyderabad&trp=false&sprop='
    return f'https://calendar.google.com/calendar/render?{urlencode(params)}'

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-events')
        else:
            messages.error(request,"Error creating event. Please try again!")
            return redirect('create_events')
    else:
        form = EventForm()
    return render(request,'organizers/create_event.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method=='POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('all-events')
        else:
            messages.error(request,"Error updating event. Please try again!")
            return redirect('edit_events', event_id=event_id)
    else:
        form = EventForm(instance=event)
    return render(request,'organizers/edit_event.html', {'form':form})


def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('all-events')

def donation(request):
    if request.method=="POST":
        donor_name = request.POST["inputDonorName"].strip()
        amount = request.POST["inputAmount"].strip()

        # event_donor_name = request.POST["inputDonorNameEvent"]
        # event_amount = request.POST["inputAmountEvent"]

        if donor_name and amount:
            Donation.objects.create(donated_name = donor_name, amount = amount, if_donated_for_event=False)
            print("General donation done successfully")
            return redirect('donation')
    else: 
        full_name = ''
        total_general_donation = 0.00
        total_event_donation = 0.00
        if request.user.is_authenticated:
            full_name = f"{request.user.first_name} {request.user.last_name}"
        get_all_donors = Donation.objects.filter(donated_name = full_name, if_donated_for_event= False)
        for donor in get_all_donors:
            total_general_donation += int(donor.amount)
        get_all_event_donors = Donation.objects.filter(donated_name = full_name, if_donated_for_event= True)
        for donor in get_all_event_donors:
            print("donor", donor)
            total_event_donation += int(donor.amount)
            print("total_event_donation", total_event_donation)
            #get list of events
        events = Event.objects.all()
        fund_raising_events = Event.objects.filter(category__name__iexact='Fundraising')
        new_events = []
        for event in fund_raising_events:
            _events = {}
            if Donation.objects.filter(event=event).exists():
                donation_obj = Donation.objects.filter(event=event)
                total_amount = 0.0
                for donation in donation_obj:
                    total_amount += float(donation.amount)
                _events['event'] = event
                _events['amount'] = total_amount
                new_events.append(_events)
            else:
                _events['event'] = event
                _events['amount'] = 0.0
                new_events.append(_events)
        return render(request, 'donation/donate.html', {'get_all_donors': get_all_donors, 'total_general_donation': total_general_donation, 'events' : events, 'total_event_donation': total_event_donation, 'fund_raising_events': new_events})

# def donation_to_event(request, event_slug):
#     context={}
#     event = Event.objects.filter(slug = event_slug)
#     if event.exists():
#         event_obj = Event.objects.get(slug = event_slug)
#         context["event"] = event_obj

#     if request.method=="POST":
#         event_donated_name = request.POST["inputDonorNameEvent"].strip()
#         event_amount = request.POST["inputAmountEvent"]
#         if event_donated_name and event_amount:
#             Donation.objects.create(donated_name = event_donated_name, amount = event_amount, if_donated_for_event=True, event=event_obj)
#             print("Event donation done successfully")
#             return redirect('donation')
#     else:
#         return render(request, 'donation/donate_to_event.html', context)

def donation_to_event(request, event_slug):
    context={}
    event = Event.objects.filter(slug = event_slug)
    if event.exists():
        event_obj = Event.objects.get(slug = event_slug)
        context["event"] = event_obj

    if request.method=="POST":
        if request.user.is_authenticated:
            event_amount = request.POST["inputAmountEvent"]
            if event_amount:
                full_name = request.user.first_name + " " + request.user.last_name
                Donation.objects.create(donated_name = full_name, amount = event_amount, if_donated_for_event=True, event=event_obj)
                messages.success(request, 'Thank you for donating to this event')
                return redirect('donation')
        else:
            messages.error(request, 'Please login to donate to this event')
            return redirect('donation')
    else:
        return render(request, 'donation/donate_to_event.html', context)