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


from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from members.forms import MemberProfileForm
from django.contrib import messages
from administration.permissions import (
    full_admin_required,
    member_management_required,
    finance_required,
    secretary_required,
)


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

        elif not user.is_active:

            error = "This account has been disabled."

        elif user.is_superuser:

            login(request, user)

            return redirect("/administration/dashboard/")

        elif user.role in [
            "SUPER_ADMIN",
            "ADMINISTRATOR",
            "SECRETARY",
            "TREASURER"
            
        ]:

            login(request, user)

            return redirect("/administration/dashboard/")

        else:

            error = (
                "You are not authorized to access the "
                "Administration Portal."
            )

    return render(
        request,
        "administration/login.html",
        {
            "error": error
        }
    )



@login_required
@full_admin_required
def dashboard(request):

    context = {

        "members": Member.objects.count(),

        "staff": User.objects.filter(is_staff=True).count(),

        "administrators": User.objects.filter(
            role__in=[
                "ADMINISTRATOR",
                "SECRETARY",
                "TREASURER",
                "PASTOR",
                "SUPER_ADMIN"
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
@member_management_required
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
@member_management_required
def member_details(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id
    )

    return render(

        request,

        "administration/member_details.html",

        {

            "member": member

        }

    )

@login_required
@member_management_required
def edit_member(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id
    )

    if request.method == "POST":

        form = MemberProfileForm(
            request.POST,
            request.FILES,
            instance=member
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Member information updated successfully."
            )

            return redirect(
                "admin-member-details",
                member.id
            )

    else:

        form = MemberProfileForm(
            instance=member
        )

    return render(

        request,

        "administration/edit_member.html",

        {

            "member": member,

            "form": form

        }

    )

@login_required
@full_admin_required
def staff(request):

    return render(
        request,
        "administration/staff.html"
    )

@full_admin_required
@login_required
def departments(request):

    return render(
        request,
        "administration/departments.html"
    )


@login_required
@secretary_required
def events(request):

    return render(
        request,
        "administration/events.html"
    )


@login_required
@secretary_required
def announcements(request):

    return render(
        request,
        "administration/announcements.html"
    )


@login_required
@secretary_required
def prayers(request):

    return render(
        request,
        "administration/prayers.html"
    )


@login_required
@secretary_required
def counselling(request):

    return render(
        request,
        "administration/counselling.html"
    )


@login_required
@finance_required
def giving(request):

    return render(
        request,
        "administration/giving.html"
    )


@login_required
@secretary_required
def reports(request):

    return render(
        request,
        "administration/reports.html"
    )


@login_required
@full_admin_required
def settings(request):

    return render(
        request,
        "administration/settings.html"
    )