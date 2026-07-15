from members.models import Member, Department
from accounts.models import User
from prayers.models import PrayerRequest
from counselling.models import CounsellingRequest
from followup.models import MemberFollowUp
from announcements.models import Announcement
from sermons.models import Sermon
from events.models import Event
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.db.models import Q


def admin_login(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            error = "Invalid username or password."

        elif user.role in [
            "ADMINISTRATOR",
            "SECRETARY",
            "TREASURER",
            "PASTOR",
        ]:

            login(request, user)

            return redirect("/administration/dashboard/")

        else:

            error = "You are not authorized to access the Administration Portal."

    return render(
        request,
        "administration/login.html",
        {
            "error": error
        }
    )



@login_required
def dashboard(request):

    context = {

        "members": Member.objects.count(),

        "staff": User.objects.filter(is_staff=True).count(),

        "administrators": User.objects.filter(
            role__in=[
                "Administrator",
                "Secretary",
                "Treasurer",
                "Pastor"
            ]
        ).count(),

        "departments": Department.objects.count(),

        "events": Event.objects.count(),

        "announcements": Announcement.objects.count(),

        "sermons": Sermon.objects.count(),

        "prayer_requests": PrayerRequest.objects.count(),

        "counselling": CounsellingRequest.objects.count(),

        "followups": MemberFollowUp.objects.count(),

    }

    return render(
        request,
        "administration/dashboard.html",
        context
    )



@login_required
def members(request):

    members = Member.objects.select_related(
        "user",
        "department",
        "role"
    )

    search = request.GET.get("search")

    department = request.GET.get("department")

    status = request.GET.get("status")

    if search:

        members = members.filter(

            Q(first_name__icontains=search) |

            Q(last_name__icontains=search) |

            Q(phone_number__icontains=search) |

            Q(email__icontains=search)

        )

    if department:

        members = members.filter(

            department_id=department

        )

    if status:

        members = members.filter(

            status=status

        )

    members = members.order_by(

        "first_name"

    )

    from members.models import Department

    departments = Department.objects.all()

    return render(

        request,

        "administration/members.html",

        {

            "members": members,

            "departments": departments,

            "search": search,

            "selected_department": department,

            "selected_status": status,

        }

    )

@login_required
def staff(request):

    return render(
        request,
        "administration/staff.html"
    )


@login_required
def departments(request):

    return render(
        request,
        "administration/departments.html"
    )


@login_required
def events(request):

    return render(
        request,
        "administration/events.html"
    )


@login_required
def announcements(request):

    return render(
        request,
        "administration/announcements.html"
    )


@login_required
def prayers(request):

    return render(
        request,
        "administration/prayers.html"
    )


@login_required
def counselling(request):

    return render(
        request,
        "administration/counselling.html"
    )


@login_required
def giving(request):

    return render(
        request,
        "administration/giving.html"
    )


@login_required
def reports(request):

    return render(
        request,
        "administration/reports.html"
    )


@login_required
def settings(request):

    return render(
        request,
        "administration/settings.html"
    )