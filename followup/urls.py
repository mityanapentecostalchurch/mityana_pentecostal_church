from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.followup_queue,
        name='followup-queue'
    ),

    path(
        '<int:followup_id>/',
        views.followup_detail,
        name='followup-detail'
    ),

    path(
        '<int:followup_id>/complete/',
        views.complete_followup,
        name='followup-complete'
    ),

    path(
        '<int:followup_id>/notes/',
        views.update_notes,
        name='followup-notes'
    ),

    path(
        '<int:followup_id>/visit/',
        views.schedule_visit,
        name='schedule-visit'
    ),

    path(
        '<int:followup_id>/visit/complete/',
        views.complete_visit,
        name='complete-visit'
    ),

]