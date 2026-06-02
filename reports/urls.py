from django.urls import path

from .views import (
    membership_report,
    attendance_report,
    finance_report,
    membership_pdf,
    finance_pdf,
    finance_csv,
    membership_csv,
    attendance_pdf,
    attendance_csv,
    contributions_pdf,
    contributions_csv,
    activity_pdf,
    activity_csv,
    events_pdf,
    events_csv,
    
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

    path(
        'membership/pdf/',
        membership_pdf,
        name='membership_pdf'
    ),

    path(
        'finance/pdf/',
        finance_pdf,
        name='finance_pdf'
    ),
    path(
        'finance/csv/',
        finance_csv,
        name='finance_csv'
    ),

    path(
        'membership/csv/',
        membership_csv,
        name='membership_csv'
    ),
    path('attendance/pdf/', attendance_pdf),
    path('attendance/csv/', attendance_csv),

    path('contributions/pdf/', contributions_pdf),
    path('contributions/csv/', contributions_csv),

    path('activity/pdf/', activity_pdf),
    path('activity/csv/', activity_csv),

    path('events/pdf/', events_pdf),
    path('events/csv/', events_csv),

]