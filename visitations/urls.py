from django.urls import path

from . import views


urlpatterns = [

    path(

        '',

        views.visit_queue,

        name='visit-queue'

    ),

    path(

        'new/',

        views.new_visit,

        name='new-visit'

    ),

    path(

        '<int:visit_id>/',

        views.visit_detail,

        name='visit-detail'

    ),

    path(

        '<int:visit_id>/complete/',

        views.complete_visit,

        name='visit-complete'

    ),

]