from django.urls import path
from .views import home, about, leadership, contact

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('leadership/', leadership, name='leadership'),
    path('contact/', contact, name='contact'),
]