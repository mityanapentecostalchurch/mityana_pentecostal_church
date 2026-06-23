
from django.urls import path

from .views import (
    create_prayer_request,
    my_prayer_requests,
)

urlpatterns = [

    path(
        'new/',
        create_prayer_request,
        name='new-prayer'
    ),

    path(
        'my/',
        my_prayer_requests,
        name='my-prayer-requests'
    ),

]