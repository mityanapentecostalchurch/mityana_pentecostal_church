# members/urls.py

from django.urls import path
# from .views import member_register, member_dashboard

from .views import (
    member_register,
    member_dashboard,
    member_login,
    edit_profile,
    member_logout,
    change_password,
    notifications,
)

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

    path(
        'login/',
        member_login,
        name='member-login'
    ),

    path(
        'profile/edit/',
        edit_profile,
        name='edit-profile'
    ),

    path(
        'logout/',
        member_logout,
        name='member-logout'
    ),

    path(
        'change-password/',
        change_password,
        name='change-password'
    ),

    path(
        'notifications/',
        notifications,
        name='notifications'
    ),
]