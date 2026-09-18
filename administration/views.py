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
from administration.forms import (
    StaffCreateForm,
    StaffUpdateForm,
    DepartmentForm,
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

    staff_members = User.objects.filter(
        role__in=[
            "ADMINISTRATOR",
            "PASTOR",
            "MINISTRY_LEADER",
            "INTERCESSOR",
        ]
    ).exclude(
        is_superuser=True
    ).order_by(
        "first_name",
        "last_name"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    role = request.GET.get(
        "role",
        ""
    ).strip()

    if search:

        staff_members = staff_members.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(phone_number__icontains=search)
            | Q(position__icontains=search)
            | Q(department__icontains=search)
        )

    if role:

        staff_members = staff_members.filter(
            role=role
        )

    return render(
        request,
        "administration/staff.html",
        {
            "staff_members": staff_members,
            "search": search,
            "selected_role": role,
        }
    )

@login_required
@full_admin_required
def add_staff(request):

    if request.method == "POST":

        form = StaffCreateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                f"{user.full_name()} has been added successfully."
            )

            return redirect(
                "admin-staff"
            )

    else:

        form = StaffCreateForm()

    return render(
        request,
        "administration/staff_form.html",
        {
            "form": form,
            "title": "Add Staff Member",
            "button_text": "Create Staff Account",
        }
    )


@login_required
@full_admin_required
def staff_details(request, staff_id):

    staff_member = get_object_or_404(
        User,
        id=staff_id
    )

    if staff_member.is_superuser:

        messages.error(
            request,
            "The system administrator account cannot be managed here."
        )

        return redirect(
            "admin-staff"
        )

    return render(
        request,
        "administration/staff_details.html",
        {
            "staff_member": staff_member
        }
    )


@login_required
@full_admin_required
def edit_staff(request, staff_id):

    staff_member = get_object_or_404(
        User,
        id=staff_id
    )

    if staff_member.is_superuser:

        messages.error(
            request,
            "The system administrator account cannot be edited here."
        )

        return redirect(
            "admin-staff"
        )

    if request.method == "POST":

        form = StaffUpdateForm(
            request.POST,
            request.FILES,
            instance=staff_member
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Staff information updated successfully."
            )

            return redirect(
                "admin-staff-details",
                staff_id=staff_member.id
            )

    else:

        form = StaffUpdateForm(
            instance=staff_member
        )

    return render(
        request,
        "administration/staff_form.html",
        {
            "form": form,
            "title": "Edit Staff Member",
            "button_text": "Save Changes",
            "staff_member": staff_member,
        }
    )


@login_required
@full_admin_required
def toggle_staff_status(request, staff_id):

    staff_member = get_object_or_404(
        User,
        id=staff_id
    )

    if staff_member.is_superuser:

        messages.error(
            request,
            "The system administrator account cannot be deactivated here."
        )

        return redirect(
            "admin-staff"
        )

    if request.method == "POST":

        staff_member.is_active = not staff_member.is_active

        staff_member.save(
            update_fields=["is_active"]
        )

        if staff_member.is_active:

            messages.success(
                request,
                "Staff account activated successfully."
            )

        else:

            messages.success(
                request,
                "Staff account deactivated successfully."
            )

    return redirect(
        "admin-staff"
    )

@login_required
@full_admin_required
def departments(request):

    departments_list = Department.objects.all().order_by(
        "name"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        departments_list = departments_list.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
        )

    for department in departments_list:

        department.member_count = Member.objects.filter(
            department=department
        ).count()

    return render(
        request,
        "administration/departments.html",
        {
            "departments": departments_list,
            "search": search,
        }
    )
@login_required
@full_admin_required
def add_department(request):

    if request.method == "POST":

        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():

            department = form.save()

            messages.success(
                request,
                f"{department.name} was created successfully."
            )

            return redirect(
                "admin-departments"
            )

    else:

        form = DepartmentForm()

    return render(
        request,
        "administration/department_form.html",
        {
            "form": form,
            "title": "Add Department",
            "button_text": "Create Department",
        }
    )


@login_required
@full_admin_required
def department_details(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    members_count = Member.objects.filter(
        department=department
    ).count()

    staff_count = User.objects.filter(
        department=department.name
    ).exclude(
        is_superuser=True
    ).count()

    return render(
        request,
        "administration/department_details.html",
        {
            "department": department,
            "members_count": members_count,
            "staff_count": staff_count,
        }
    )


@login_required
@full_admin_required
def edit_department(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == "POST":

        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Department updated successfully."
            )

            return redirect(
                "admin-department-details",
                department_id=department.id
            )

    else:

        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        "administration/department_form.html",
        {
            "form": form,
            "title": "Edit Department",
            "button_text": "Save Changes",
            "department": department,
        }
    )


@login_required
@full_admin_required
def delete_department(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == "POST":

        members_count = Member.objects.filter(
            department=department
        ).count()

        if members_count > 0:

            messages.error(
                request,
                f"Cannot delete {department.name} because "
                f"{members_count} member(s) are assigned to it."
            )

            return redirect(
                "admin-department-details",
                department_id=department.id
            )

        department_name = department.name

        department.delete()

        messages.success(
            request,
            f"{department_name} was deleted successfully."
        )

        return redirect(
            "admin-departments"
        )

    return redirect(
        "admin-department-details",
        department_id=department.id
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