from django.urls import path

from . import views


urlpatterns = [

    path(
        'new/',
        views.new_counselling_request,
        name='new-counselling'
    ),

    path(
        'my/',
        views.my_counselling_requests,
        name='my-counselling'
    ),

    path(
        'queue/',
        views.counselling_queue,
        name='counselling-queue'
    ),

    path(
        '<int:request_id>/',
        views.counselling_detail,
        name='counselling-detail'
    ),

    path(
        '<int:request_id>/schedule/',
        views.schedule_counselling,
        name='schedule-counselling'
    ),

]