from django.urls import path

from .views import (
    staff_dashboard,
    prayer_queue,
    staff_login,
    prayer_detail,
    mark_prayed,
    add_prayer_note,
    edit_prayer_note,
    delete_prayer_note,
)
from counselling import views as counselling_views

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

    path(
        'prayers/<int:prayer_id>/',
        prayer_detail,
        name='prayer-detail'
    ),

    path(
        'prayers/<int:prayer_id>/prayed/',
        mark_prayed,
        name='mark-prayed'
    ),

    path(
        'prayers/<int:prayer_id>/note/',
        add_prayer_note,
        name='add-note'
    ),

    path(
    'prayers/note/<int:note_id>/edit/',
        edit_prayer_note,
        name='edit-prayer-note'
    ),

    path(
        'prayers/note/<int:note_id>/delete/',
        delete_prayer_note,
        name='delete-prayer-note'
    ),

    path(
        'counselling/',
        counselling_views.counselling_queue,
        name='staff-counselling'
    ),

]