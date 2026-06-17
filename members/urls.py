# members/urls.py

from django.urls import path
from .views import member_register, member_dashboard

urlpatterns = [

    path(
        'register/',
        member_register,
        name='member-register'
    ),

    path(
        'dashboard/',
        member_dashboard,
        name='member-dashboard'
    ),

]