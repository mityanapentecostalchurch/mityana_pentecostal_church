# api/urls.py

from django.urls import path

from .views import ( MemberListAPIView, DepartmentListAPIView, EventListAPIView, 
                    AnnouncementListAPIView, SermonListAPIView, CurrentUserAPIView, 
                    AttendanceAPIView, ServiceListAPIView, ContributionAPIView, 
                    DashboardAPIView, MemberDetailAPIView,
)

urlpatterns = [

    path('members/', MemberListAPIView.as_view(), name='api-members'),
    path('members/<int:pk>/', MemberDetailAPIView.as_view(), name='api-member-detail'),
    path('departments/', DepartmentListAPIView.as_view(), name='api-departments'),
    path('events/', EventListAPIView.as_view(), name='api-events'),
    path('announcements/', AnnouncementListAPIView.as_view(), name='api-announcements'),
    path('sermons/', SermonListAPIView.as_view(), name='api-sermons'),
    path('me/', CurrentUserAPIView.as_view(), name='api-me'),
    path('attendance/', AttendanceAPIView.as_view(), name='api-attendance'),
    path('services/', ServiceListAPIView.as_view(), name='api-services'),
    path('contributions/', ContributionAPIView.as_view(), name='api-contributions'),
    path('me/', CurrentUserAPIView.as_view(), name='api-me'),
    path('dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),

]