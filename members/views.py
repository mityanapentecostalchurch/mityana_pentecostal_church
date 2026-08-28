from django.shortcuts import render, redirect
from django.contrib.auth import (
    get_user_model,
    login,
    logout,
    authenticate,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
)
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import (
    MemberRegistrationForm,
    MemberProfileForm,
)

from .models import Member

from counselling.models import CounsellingRequest
from followup.models import MemberFollowUp
from followup.models import MemberNotification
from sermons.models import Sermon


User = get_user_model()


def normalize_phone(phone):
    if not phone:
        return ""

    phone = (
        phone
        .strip()
        .replace(" ", "")
        .replace("-", "")
    )

    if phone.startswith("+256"):
        return phone

    if phone.startswith("256"):
        return "+" + phone

    if phone.startswith("0") and len(phone) == 10:
        return "+256" + phone[1:]

    return phone


def member_login(request):

    error = None

    if request.method == "POST":

        phone_number = request.POST.get(
            "phone_number",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        if not phone_number or not password:

            error = (
                "Please enter your phone number "
                "and password."
            )

            return render(
                request,
                "members/login.html",
                {
                    "error": error
                }
            )

        phone = normalize_phone(
            phone_number
        )

        member = (
            Member.objects
            .select_related("user")
            .filter(
                phone_number=phone,
                is_active=True
            )
            .first()
        )

        if not member:

            error = (
                "No active member account was found "
                "with this phone number."
            )

            return render(
                request,
                "members/login.html",
                {
                    "error": error
                }
            )

        if not member.user:

            error = (
                "This member account is not linked "
                "to a user account. Please contact "
                "the church administrator."
            )

            return render(
                request,
                "members/login.html",
                {
                    "error": error
                }
            )

        user = authenticate(
            request,
            username=member.user.username,
            password=password
        )

        if user is None:

            error = (
                "Incorrect phone number or password."
            )

            return render(
                request,
                "members/login.html",
                {
                    "error": error
                }
            )

        if not user.is_active:

            error = (
                "This account is currently inactive. "
                "Please contact the church administrator."
            )

            return render(
                request,
                "members/login.html",
                {
                    "error": error
                }
            )

        login(
            request,
            user,
            backend=(
                "django.contrib.auth.backends.ModelBackend"
            )
        )

        if user.is_superuser:
            return redirect(
                "/administration/"
            )

        if user.is_staff:
            return redirect(
                "/staff/"
            )

        return redirect(
            "/members/dashboard/"
        )

    return render(
        request,
        "members/login.html",
        {
            "error": error
        }
    )


def forgot_password(request):

    if request.method == "POST":

        form = PasswordResetForm(
            request.POST
        )

        if form.is_valid():

            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=None,
                email_template_name=(
                    "registration/"
                    "password_reset_email.html"
                ),
                subject_template_name=(
                    "registration/"
                    "password_reset_subject.txt"
                ),
            )

            messages.success(
                request,
                (
                    "If an account exists with this email, "
                    "a password reset link has been sent."
                )
            )

            return redirect(
                "member-login"
            )

    else:

        form = PasswordResetForm()

    return render(
        request,
        "members/forgot_password.html",
        {
            "form": form
        }
    )


@login_required
def member_dashboard(request):

    member = getattr(
        request.user,
        "member",
        None
    )

    completion = 0

    if member:

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

        completed = sum(
            1
            for field in fields
            if field
        )

        if total:
            completion = int(
                (completed / total) * 100
            )

    notifications = (
        request.user.notifications
        .order_by("-created_at")[:5]
    )

    latest_followup = (
        MemberFollowUp.objects
        .filter(
            member=request.user
        )
        .order_by("-created_at")
        .first()
    )

    unread_notifications = (
        MemberNotification.objects
        .filter(
            member=request.user,
            is_read=False
        )
        .count()
    )

    latest_sermon = (
        Sermon.objects
        .filter(is_published=True)
        .order_by("-created_at")
        .first()
    )

    return render(
        request,
        "members/dashboard.html",
        {
            "member": member,
            "completion": completion,
            "notifications": notifications,
            "latest_followup": latest_followup,
            "unread_notifications": unread_notifications,
            "latest_sermon": latest_sermon,
        }
    )


def member_register(request):

    if request.method == "POST":

        form = MemberRegistrationForm(
            request.POST
        )

        if form.is_valid():

            phone = normalize_phone(
                form.cleaned_data["phone_number"]
            )

            email = form.cleaned_data.get(
                "email"
            )

            if email:
                email = email.strip().lower()

            password = form.cleaned_data["password"]

            if Member.objects.filter(
                phone_number=phone
            ).exists():

                form.add_error(
                    "phone_number",
                    (
                        "An account already exists "
                        "with this phone number. "
                        "Please login instead."
                    )
                )

                return render(
                    request,
                    "members/register.html",
                    {
                        "form": form
                    }
                )

            if email:

                if User.objects.filter(
                    email__iexact=email
                ).exists():

                    form.add_error(
                        "email",
                        (
                            "An account already exists "
                            "with this email address. "
                            "Please login instead."
                        )
                    )

                    return render(
                        request,
                        "members/register.html",
                        {
                            "form": form
                        }
                    )

            username = phone

            user = User.objects.create_user(
                username=username,
                email=email or "",
                password=password
            )

            member = form.save(
                commit=False
            )

            member.phone_number = phone
            member.email = email or ""
            member.user = user
            member.save()

            pastor = User.objects.filter(
                role="PASTOR",
                is_active=True
            ).first()

            if pastor:

                MemberFollowUp.objects.create(
                    member=user,
                    assigned_to=pastor,
                    followup_type="NEW_MEMBER",
                    reason=(
                        "Welcome the new member, "
                        "introduce them to the church, "
                        "encourage participation in "
                        "worship services, Bible study "
                        "and ministries."
                    )
                )

                MemberNotification.objects.create(
                    member=user,
                    title=(
                        "Welcome to "
                        "Mityana Pentecostal Church"
                    ),
                    message=(
                        "Welcome to the Mityana Pentecostal "
                        "Church family. "
                        f"{pastor.get_full_name() or pastor.username} "
                        "has been assigned to welcome "
                        "and support you."
                    )
                )

            else:

                MemberNotification.objects.create(
                    member=user,
                    title=(
                        "Welcome to "
                        "Mityana Pentecostal Church"
                    ),
                    message=(
                        "Welcome to the Mityana Pentecostal "
                        "Church family. Your registration "
                        "has been received successfully."
                    )
                )

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:

                login(
                    request,
                    authenticated_user,
                    backend=(
                        "django.contrib.auth.backends.ModelBackend"
                    )
                )

                messages.success(
                    request,
                    (
                        "Your account has been created "
                        "successfully. Welcome to "
                        "Mityana Pentecostal Church."
                    )
                )

                return redirect(
                    "/members/dashboard/"
                )

            messages.error(
                request,
                (
                    "Your account was created, but "
                    "automatic login failed. "
                    "Please login using your phone number."
                )
            )

            return redirect(
                "/members/login/"
            )

    else:

        form = MemberRegistrationForm()

    return render(
        request,
        "members/register.html",
        {
            "form": form
        }
    )


@login_required
def edit_profile(request):

    user = request.user

    member = getattr(
        user,
        "member",
        None
    )

    if member is None:

        member = Member(
            user=user,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            email=user.email or ""
        )

    if request.method == "POST":

        form = MemberProfileForm(
            request.POST,
            request.FILES,
            instance=member
        )

        if form.is_valid():

            member = form.save(
                commit=False
            )

            member.user = user

            member.first_name = request.POST.get(
                "first_name",
                member.first_name
            )

            member.last_name = request.POST.get(
                "last_name",
                member.last_name
            )

            member.email = (
                request.POST.get(
                    "email",
                    user.email
                )
                or user.email
            )

            member.save()

            user.first_name = request.POST.get(
                "first_name",
                user.first_name
            )

            user.last_name = request.POST.get(
                "last_name",
                user.last_name
            )

            submitted_email = request.POST.get(
                "email"
            )

            if submitted_email:
                user.email = (
                    submitted_email.strip().lower()
                )

            if request.FILES.get(
                "profile_photo"
            ):

                user.profile_photo = (
                    request.FILES[
                        "profile_photo"
                    ]
                )

            user.save()

            return redirect(
                "/members/dashboard/"
            )

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
            "member": member,
        }
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

            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect(
                "/members/dashboard/"
            )

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

    counselling = (
        CounsellingRequest.objects
        .filter(
            member=request.user,
            status="SCHEDULED"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "members/notifications.html",
        {
            "counselling": counselling
        }
    )