# members/views.py

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth import (
    get_user_model,
    login,
)


from .forms import (
    MemberRegistrationForm,
    MemberProfileForm
)
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.contrib.auth import authenticate
User = get_user_model()

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from counselling.models import CounsellingRequest
from followup.models import MemberFollowUp
from accounts.models import User
from followup.models import MemberNotification
from sermons.models import Sermon


# @login_required
# def member_dashboard(request):

#     # member = request.user.member
#     try:
#         member = request.user.member
#     except Exception:
#         member = None
    

#     return render(
#         request,
#         'members/dashboard.html',
#         {
#             'member': member
#         }
#     )
def member_login(request):

    error = None

    if request.method == "POST":

        email = request.POST.get("email")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            if user.is_superuser:

                return redirect('/administration/')

            elif user.is_staff:

                return redirect('/staff/')

            else:

                return redirect(
                    '/members/dashboard/'
                )

        else:

            error = (
                "Invalid email or password."
            )

    return render(
        request,
        "members/login.html",
        {
            "error": error
        }
    )

@login_required
def member_dashboard(request):

    # member = request.user.member
    member = getattr(
        request.user,
        'member',
        None
    )

    completed = 0

    fields = [

        member.phone_number,
        member.email,
        member.address,
        member.next_of_kin,
        member.next_of_kin_contact,
        member.occupation,
        member.education_level,
        member.department,
        member.date_saved,
        member.is_baptized,
        member.former_church,
        member.previous_ministry,
        

    ]

    total = len(fields)

    for field in fields:

        if field:
            completed += 1

    completion = int(
        (completed / total) * 100
    )
    notifications = request.user.notifications.order_by(
            '-created_at'
    )[:5]

    latest_followup = MemberFollowUp.objects.filter(
        member=request.user
    ).order_by(
        '-created_at'
    ).first()

    unread_notifications = MemberNotification.objects.filter(
        member=request.user,
        is_read=False
    ).count()

    latest_sermon = Sermon.objects.filter(
        is_published=True
    ).first()

    return render(
        request,
        'members/dashboard.html',
        {
            'member': member,
            'completion': completion,
            'notifications': notifications,
            'latest_followup': latest_followup,
            'unread_notifications': unread_notifications,
            'latest_sermon': latest_sermon,
        }
    )

def member_register(request):

    if request.method == "POST":

        form = MemberRegistrationForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():

                form.add_error(
                    'email',
                    'An account with this email already exists.'
                )

            else:

                # -------------------------
                # Create Login Account
                # -------------------------

                user = User.objects.create_user(

                    username=email,

                    email=email,

                    password=password

                )

                # -------------------------
                # Create Member Profile
                # -------------------------

                member = form.save(commit=False)

                member.user = user

                member.save()

                # -------------------------
                # Assign Pastor
                # -------------------------

                pastor = User.objects.filter(
                    role='PASTOR'
                ).first()

                if pastor:

                    MemberFollowUp.objects.create(

                        member=user,

                        assigned_to=pastor,

                        followup_type='NEW_MEMBER',

                        reason=(
                            "Welcome the new member, introduce them "
                            "to the church, encourage participation "
                            "in worship services, Bible study and ministries."
                        )

                    )

                    MemberNotification.objects.create(

                        member=user,

                        title="Welcome to Mityana Pentecostal Church",

                        message=(
                            f"Welcome to the Mityana Pentecostal Church family. "
                            f"{pastor.get_full_name() or pastor.username} "
                            "has been assigned to welcome and support you. "
                            "You may be contacted soon for a pastoral follow-up."
                        )

                    )

                else:

                    MemberNotification.objects.create(

                        member=user,

                        title="Welcome to Mityana Pentecostal Church",

                        message=(
                            "Welcome to the Mityana Pentecostal Church family. "
                            "Your registration has been received successfully. "
                            "A pastor will be assigned to you shortly."
                        )

                    )

                # -------------------------
                # Login Member
                # -------------------------

                login(request, user)

                return redirect(
                    '/members/dashboard/'
                )

    else:

        form = MemberRegistrationForm()

    return render(

        request,

        'members/register.html',

        {

            'form': form

        }

    )

@login_required
def edit_profile(request):

    member = request.user.member
    user = request.user

    if request.method == "POST":

        form = MemberProfileForm(
            request.POST,
            request.FILES,
            instance=member
        )

        if form.is_valid():

            form.save()

            # Upload profile photo
            if request.FILES.get("profile_photo"):
                user.profile_photo = request.FILES["profile_photo"]

            user.first_name = request.POST.get(
                "first_name",
                user.first_name
            )

            user.last_name = request.POST.get(
                "last_name",
                user.last_name
            )

            user.save()
            member.first_name = user.first_name
            member.last_name = user.last_name
            member.email = user.email

            member.save()

            return redirect("/members/dashboard/")

    else:

        form = MemberProfileForm(
            instance=member
        )

    return render(
        request,
        "members/edit_profile.html",
        {
            "form": form,
            "user": user,
        },
    )

@login_required
def member_logout(request):

    logout(request)

    return redirect("/")


@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            return redirect("/members/dashboard/")

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "members/change_password.html",
        {
            "form": form
        }
    )


@login_required
def notifications(request):

    counselling = CounsellingRequest.objects.filter(
        member=request.user,
        status="SCHEDULED"
    ).order_by("-created_at")

    return render(
        request,
        "members/notifications.html",
        {
            "counselling": counselling
        }
    )