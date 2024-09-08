from django.urls import path
from adopt.views import list_pets, list_breeds, create_pet, detail_pet, adopt_pet, adoption_success, manage_pets, edit_pet, delete_pet, adopt_requests, request_accepted, request_cancelled

urlpatterns = [
    #path('',  home, name='home')
    path('list-pets', list_pets, name='list-pets'),
    path('create-pet', create_pet, name='create-pet'),
    path('edit-pet/<str:pet_slug>/', edit_pet, name='edit-pet'),
    path('delete-pet/<str:pet_slug>/', delete_pet, name='delete-pet'),
    path('list-breeds', list_breeds, name='list-breeds'),
    path('<str:pet_slug>/', detail_pet, name='detail-pet'),
    path('<slug:slug>/adopt/', adopt_pet, name='adopt-pet'),
    path('adoption-success/', adoption_success, name='adoption_success'),
    path('manage/<int:user_id>/pets', manage_pets, name='manage-pets'),
    path('manage/<int:user_id>/adopt-requests/', adopt_requests, name='adopt-requests'),
    path('<int:request_id>/<int:user_id>/request-accepted/', request_accepted, name='request-accepted'),
    path('<int:request_id>/<int:user_id>/request-cancelled/', request_cancelled, name='request-cancelled')
]