# api/urls.py

from django.urls import path

from .views import ( MemberListAPIView, DepartmentListAPIView, EventListAPIView, 
                    AnnouncementListAPIView, SermonListAPIView, CurrentUserAPIView,
)

urlpatterns = [

    path('members/', MemberListAPIView.as_view(), name='api-members'),
    path('departments/', DepartmentListAPIView.as_view(), name='api-departments'),
    path('events/', EventListAPIView.as_view(), name='api-events'),
    path('announcements/', AnnouncementListAPIView.as_view(), name='api-announcements'),
    path('sermons/', SermonListAPIView.as_view(), name='api-sermons'),
    path('me/', CurrentUserAPIView.as_view(), name='api-me'),

]