from django.shortcuts import render, redirect, get_object_or_404
from recycle.models import RecycleRequest, RecycleRequestStatus
from django.contrib.auth.models import User
from recycle.forms import LoggedUserRecycleRequestForm, GuestUserRecycleRequestForm
from django.core.mail import send_mail
# Create your views here.

def create_recycle_request(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = LoggedUserRecycleRequestForm(request.POST)
            if form.is_valid():
                recycle = form.save(commit=False)
                recycle.user = request.user
                recycle.save()
                RecycleRequestStatus.objects.create(request=recycle)
                send_mail(
                    "EcoGuardian-Recycle Request",
                    f"Thank you for creating recycling request with EcoGuardians. You will gwt a comfirmation update in 2-3 days. Please check you email frequently for further updates for picking up your recycled items from you house",
                    "ecoguardian@gmail.com",
                    [recycle.user.email],
                    fail_silently=False,
            )
                return redirect('create-recycle-request')
        else:
            form = LoggedUserRecycleRequestForm()
        context['loggeduser_recycle_form'] = form
    else:
        if request.method == 'POST':
            form = GuestUserRecycleRequestForm(request.POST)
            if form.is_valid():
                recycle = form.save(commit=False)
                recycle.save()
                RecycleRequestStatus.objects.create(request=recycle)
                send_mail(
                    "EcoGuardian-Recycle Request",
                    f"Thank you for creating recycling request with EcoGuardians. You will gwt a comfirmation update in 2-3 days. Please check you email frequently for further updates for picking up your recycled items from you house",
                    "ecoguardian@gmail.com",
                    [recycle.email],
                    fail_silently=False,
            )
                return redirect('create-recycle-request')
        else:
            form = GuestUserRecycleRequestForm()
        context['guestuser_recycle_form'] = form
        
    return render(request, 'recycle_form.html', context)

def recycle_request_list(request):
    context = {}
    all_recycle_requests = RecycleRequestStatus.objects.all().order_by('-id')
    print(all_recycle_requests, "*****")
    context['all_recycle_requests'] = all_recycle_requests
    return render(request, 'recycle_list.html', context)

def recycle_request_accept(request, req_id):
    req = get_object_or_404(RecycleRequestStatus, id=req_id)
    req.status = True
    req.save()
    if req.request.user:
        send_mail(
            "Recycle Request Accepted",
            f"This is a confirmation email about the reycle requestyou made. We will soon pick up your items from your house. Our team will contact you from the number you have provided.",
            "ecoguardian@gmail.com",
            [req.request.user.email],
            fail_silently=False,
        )
    else: 
        send_mail(
            "Recycle Request Accepted",
            f"This is a confirmation email about the reycle requestyou made. We will soon pick up your items from your house. Our team will contact you from the number you have provided.",
            "ecoguardian@gmail.com",
            [req.request.user.email],
            fail_silently=False,
        )
    return redirect('recycle-request-list')


def recycle_request_reject(request, req_id):
    req = get_object_or_404(RecycleRequestStatus, id=req_id)
    req.status = False
    req.save()
    if req.request.user:
        send_mail(
            "Recycle Request Rejected",
            f"This is a confirmation email abou the reycle requestyou made. We will not be able to pick up your item. Thank you",
            "ecoguardian@gmail.com",
            [req.request.user.email],
            fail_silently=False,
        )
    else: 
        send_mail(
            "Recycle Request Rejected",
            f"This is a confirmation email abou the reycle requestyou made. We will not be able to pick up your item. Thank you",
            "ecoguardian@gmail.com",
            [req.request.user.email],
            fail_silently=False,
        )
    return redirect('recycle-request-list')