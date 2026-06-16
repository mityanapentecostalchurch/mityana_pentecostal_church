# members/urls.py

from django.urls import path
from .views import member_register

urlpatterns = [

    path(
        'register/',
        member_register,
        name='member-register'
    ),

]