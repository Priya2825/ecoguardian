from django.shortcuts import render, redirect, get_object_or_404
from adopt.models import Pet, PetBreed, PetContact, AdoptionStatus
from adopt.forms import PetForm, AdoptionForm, PetContactForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.

def list_pets(request):
    context= {}
    if request.user.is_authenticated:
        pets = Pet.objects.exclude(owner_name=request.user)
        context['pets'] = pets
    else:
        pets = Pet.objects.all()
        context['pets'] = pets

    adopted_pet_ids = AdoptionStatus.objects.filter(pet_adopt_request=True, adoption_completed=False).values_list('pet__id', flat=True)
    context['adopted_pet_ids'] = adopted_pet_ids
    return render(request, 'pets/list_pets.html', context)


def create_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.owner_name = request.user
            instance.save()
            return redirect('list-pets') #redirect to the list pets if new pets is added
    else:
        form = PetForm()
    return render(request, 'pets/create_pet.html', {'form': form})

def edit_pet(request, pet_slug):
    pet_obj = get_object_or_404(Pet, slug=pet_slug)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet_obj)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.owner_name = request.user
            instance.save()
            return redirect('manage-pets', user_id=request.user.id) #redirect to the list pets if new pets is added
    else:
        form = PetForm(instance=pet_obj)
    return render(request, 'pets/edit_pet.html', {'form': form})

def delete_pet(request, pet_slug):
    pet_obj = get_object_or_404(Pet, slug=pet_slug)
    pet_obj.delete()
    return redirect('manage-pets', user_id=request.user.id) #redirect to the list pets if new pets is added


def list_breeds(request):
    pet_breeds = PetBreed.objects.all()
    context = {
        'pet_breeds': pet_breeds
    }
    return render(request,'pet_breeds/list_breeds.html', context)

# def detail_pet(request, pet_slug):
#     context = {}
#     pet = get_object_or_404(Pet, slug=pet_slug)
#     context["pet"] = Pet
#     return render(request, 'pets/detail_pet.html', context)


def detail_pet(request, pet_slug):
    pet = get_object_or_404(Pet, slug=pet_slug)
    print(pet)  # Debugging: Check if the pet is correctly fetched
    context = {
        'pet': pet,
        'pet_images': pet.image  # If you need to use pet_images separately
    }
    adopted_pet_ids = AdoptionStatus.objects.filter(pet_adopt_request=True, adoption_completed=False).values_list('pet__id', flat=True)
    context['adopted_pet_ids'] = adopted_pet_ids
    return render(request, 'pets/detail_pet.html', context)


def adopt_pet(request, slug):
    pet = get_object_or_404(Pet, slug=slug)
    if AdoptionStatus.objects.filter(pet_adopt_request=True, pet=pet).exists():
        return redirect('list-pets')
    else:
        if request.method == 'POST':
            form = AdoptionForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.pet = pet
                instance.save()
                AdoptionStatus.objects.create(adoptee=instance, pet=pet, pet_adopt_request=True)
                send_mail(
                    "Adoption Request Update",
                    f"Thank you for showing interest to adopt {pet.name}. We will send you a confirmation email in 2-3 days.",
                    "ecoguardian@gmail.com",
                    [instance.email],
                    fail_silently=False,
            )
                # handle form submission (e.g., send an email)
                return render(request, 'pets/adoption_success.html')
        else:
            form = AdoptionForm()
        return render(request, 'pets/adopt_me.html', {'form': form, 'pet': pet})

def adoption_success(request):
    return render(request, 'pets/adoption_success.html')


def manage_pets(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=user_id)

        pets = Pet.objects.filter(owner_name = user)
        return render(request, 'pets/manage_pets.html', {'pets': pets})

def adopt_requests(request, user_id):
    context = {}
    if request.user.is_authenticated:
        user = get_object_or_404(User,id=user_id)
        adopt_requests = AdoptionStatus.objects.filter(pet__owner_name=user)
        context['adopt_requests'] = adopt_requests

        return render(request, 'pets/adopt_request.html', context)


def request_accepted(request, request_id, user_id):
    req = get_object_or_404(AdoptionStatus, id=request_id)
    req.adoption_completed = True
    req.save()
    send_mail(
                "Adoption Request Accepted",
                f"This is an confirmation email about the aoption request you have made for the {req.pet.name}. You can adopt {req.pet.name}. Please reply back for further communication.",
                "ecoguardian@gmail.com",
                [req.adoptee.email],
                fail_silently=False,
            )
    return redirect('adopt-requests', user_id= user_id)


def request_cancelled(request, request_id, user_id):
    req = get_object_or_404(AdoptionStatus, id=request_id)
    req.adoption_completed = False
    req.save()
    send_mail(
                "Adoption Request Cancelled",
                f"This is an confirmation email about the aoption request you have made for the {req.pet.name}. You cannot adopt {req.pet.name}. Please kindly check out other available pets. Thank you. ",
                "ecoguardian@gmail.com",
                [req.adoptee.email],
                fail_silently=False,
            )
    return redirect('adopt-requests', user_id= user_id)
