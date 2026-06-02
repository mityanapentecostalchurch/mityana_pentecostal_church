# reports/views.py

from django.shortcuts import render
from members.models import Member, Department


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