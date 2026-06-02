from django.shortcuts import render

from members.models import Member
from members.models import Department
from members.models import Role

from announcements.models import Announcement
from events.models import Event
from sermons.models import Sermon


from django.contrib.auth.decorators import login_required

from members.models import Member, Department, Role
from attendance.models import Attendance, Service
from giving.models import Contribution
from django.db.models import Sum


@login_required
def dashboard_home(request):

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
        'total_amount': Contribution.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )

