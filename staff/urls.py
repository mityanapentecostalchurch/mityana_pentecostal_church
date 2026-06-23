from django.urls import path

from .views import (
    staff_dashboard,
    prayer_queue,
    staff_login,
)

urlpatterns = [

    path(
        '',
        staff_dashboard,
        name='staff-dashboard'
    ),

    path(
        'login/',
        staff_login,
        name='staff-login'
    ),

    path(
        'prayers/',
        prayer_queue,
        name='staff-prayers'
    ),

]