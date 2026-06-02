# reports/urls.py

from django.urls import path
from .views import membership_report

urlpatterns = [
    path(
        'membership/',
        membership_report,
        name='membership_report'
    ),
]