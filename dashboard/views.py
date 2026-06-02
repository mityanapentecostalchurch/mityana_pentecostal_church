from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from members.models import Member, Department, Role
from announcements.models import Announcement
from events.models import Event
from sermons.models import Sermon
from attendance.models import Attendance, Service
from giving.models import Contribution


@login_required
def dashboard_home(request):

    total_amount = Contribution.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    mobile_money_total = Contribution.objects.filter(
        payment_method='MOBILE_MONEY'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    cash_total = Contribution.objects.filter(
        payment_method='CASH'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    recent_members = Member.objects.order_by(
    '-created_at'
    )[:5]

    recent_contributions = Contribution.objects.order_by(
        '-contribution_date'
    )[:5]

    upcoming_events = Event.objects.filter(
        is_active=True
    ).order_by(
        'event_date'
    )[:5]

    recent_announcements = Announcement.objects.filter(
        is_active=True
    ).order_by(
        '-created_at'
    )[:5]

    context = {
        'member_count': Member.objects.count(),
        'department_count': Department.objects.count(),
        'role_count': Role.objects.count(),

        'announcement_count': Announcement.objects.count(),
        'event_count': Event.objects.count(),
        'sermon_count': Sermon.objects.count(),

        'attendance_count': Attendance.objects.count(),
        'service_count': Service.objects.count(),

        'total_contributions': Contribution.objects.count(),

        'total_amount': total_amount,
        'mobile_money_total': mobile_money_total,
        'cash_total': cash_total,
        'recent_members': recent_members,
        'recent_contributions': recent_contributions,
        'upcoming_events': upcoming_events,
        'recent_announcements': recent_announcements,
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )