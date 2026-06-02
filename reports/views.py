# reports/views.py

from django.shortcuts import render
from members.models import Member, Department
from attendance.models import Attendance, Service
from giving.models import Contribution
from django.db.models import Sum


def membership_report(request):

    departments = Department.objects.all()

    context = {
        'member_count': Member.objects.count(),
        'active_members':
            Member.objects.filter(
                status='ACTIVE'
            ).count(),

        'inactive_members':
            Member.objects.filter(
                status='INACTIVE'
            ).count(),

        'visitor_count':
            Member.objects.filter(
                status='VISITOR'
            ).count(),

        'departments': departments,
    }

    return render(
        request,
        'reports/membership_report.html',
        context
    )

def attendance_report(request):

    context = {
        'attendance_count':
            Attendance.objects.count(),

        'service_count':
            Service.objects.count(),

        'present_count':
            Attendance.objects.filter(
                status='PRESENT'
            ).count(),

        'absent_count':
            Attendance.objects.filter(
                status='ABSENT'
            ).count(),

        'excused_count':
            Attendance.objects.filter(
                status='EXCUSED'
            ).count(),
    }

    return render(
        request,
        'reports/attendance_report.html',
        context
    )


def finance_report(request):

    total_amount = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    cash_total = Contribution.objects.filter(
        payment_method='CASH'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    mobile_money_total = Contribution.objects.filter(
        payment_method='MOBILE_MONEY'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    bank_total = Contribution.objects.filter(
        payment_method='BANK'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        'total_amount': total_amount,
        'cash_total': cash_total,
        'mobile_money_total': mobile_money_total,
        'bank_total': bank_total,
    }

    return render(
        request,
        'reports/finance_report.html',
        context
    )