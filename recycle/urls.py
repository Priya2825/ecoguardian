from django.urls import path
from recycle.views import *

urlpatterns =[
    path('create/', create_recycle_request, name='create-recycle-request'),
    path('create/list/', recycle_request_list, name='recycle-request-list'),
    path('request/<int:req_id>/accept/', recycle_request_accept, name='recycle-request-accept'),
    path('request/<int:req_id>/reject/', recycle_request_reject, name='recycle-request-reject'),
]