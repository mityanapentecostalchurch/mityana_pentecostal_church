from django.urls import path

from .views import (
    membership_report,
    attendance_report,
    finance_report,
)

urlpatterns = [

    path(
        'membership/',
        membership_report,
        name='membership_report'
    ),

    path(
        'attendance/',
        attendance_report,
        name='attendance_report'
    ),

    path(
        'finance/',
        finance_report,
        name='finance_report'
    ),
]