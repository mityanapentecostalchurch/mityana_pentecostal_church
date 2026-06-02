from django.urls import path
from .views import home, about, leadership, contact, sermon_list, announcement_list, event_list

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('leadership/', leadership, name='leadership'),
    path('contact/', contact, name='contact'),
    path('sermons/', sermon_list, name='sermons'),
    path('announcements/', announcement_list, name='announcements'),
    path('events/', event_list, name='events'
),

]