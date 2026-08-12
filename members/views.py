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
from .models import Member
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from counselling.models import CounsellingRequest
from followup.models import MemberFollowUp
from accounts.models import User
from followup.models import MemberNotification
from sermons.models import Sermon
from .models import Member, PhoneOTP
import random

from datetime import timedelta

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import views as auth_views


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

                email_template_name=
                "registration/password_reset_email.html",

                subject_template_name=
                "registration/password_reset_subject.txt",

                domain_override=None,
            )

            messages.success(
                request,
                "If an account exists with this email, "
                "a password reset link has been sent."
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


def phone_login(request):

    return render(
        request,
        "members/login_phone.html"
    )


def send_phone_otp(request):

    error = None

    if request.method != "POST":

        return redirect(
            "phone-login"
        )

    phone_number = request.POST.get(
        "phone_number",
        ""
    ).strip()

    # ---------------------------------------------------------
    # Check phone number
    # ---------------------------------------------------------

    if not phone_number:

        error = "Please enter your phone number."

        return render(
            request,
            "members/login_phone.html",
            {
                "error": error
            }
        )

    # ---------------------------------------------------------
    # Find active members
    # ---------------------------------------------------------

    members = Member.objects.filter(
        phone_number=phone_number,
        is_active=True
    )

    # ---------------------------------------------------------
    # No member found
    # ---------------------------------------------------------

    if not members.exists():

        error = (
            "No active church member was found "
            "with this phone number."
        )

        return render(
            request,
            "members/login_phone.html",
            {
                "error": error
            }
        )

    # ---------------------------------------------------------
    # Duplicate phone number
    # ---------------------------------------------------------

    if members.count() > 1:

        error = (
            "This phone number is associated with "
            "more than one member account. "
            "Please contact the church office "
            "to update your phone number."
        )

        return render(
            request,
            "members/login_phone.html",
            {
                "error": error
            }
        )

    # ---------------------------------------------------------
    # Get the member
    # ---------------------------------------------------------

    member = members.first()

    # ---------------------------------------------------------
    # Check linked User account
    # ---------------------------------------------------------

    if not member.user:

        error = (
            "Your church member profile is not yet "
            "linked to a login account. Please contact "
            "the church office."
        )

        return render(
            request,
            "members/login_phone.html",
            {
                "error": error
            }
        )

    # ---------------------------------------------------------
    # Generate six-digit OTP
    # ---------------------------------------------------------

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    # ---------------------------------------------------------
    # OTP expires after 5 minutes
    # ---------------------------------------------------------

    expires_at = timezone.now() + timedelta(
        minutes=5
    )

    # ---------------------------------------------------------
    # Remove old unverified OTPs
    # ---------------------------------------------------------

    PhoneOTP.objects.filter(
        phone_number=phone_number,
        is_verified=False
    ).delete()

    # ---------------------------------------------------------
    # Create new OTP
    # ---------------------------------------------------------

    PhoneOTP.objects.create(
        phone_number=phone_number,
        otp=otp,
        expires_at=expires_at
    )

    # ---------------------------------------------------------
    # DEVELOPMENT ONLY
    #
    # Later this will be replaced by an SMS provider.
    # ---------------------------------------------------------

    print(
        "======================================"
    )

    print(
        f"MPC PHONE OTP for {phone_number}: {otp}"
    )

    print(
        f"OTP expires at: {expires_at}"
    )

    print(
        "======================================"
    )

    # ---------------------------------------------------------
    # Remember phone number in session
    # ---------------------------------------------------------

    request.session[
        "otp_phone_number"
    ] = phone_number

    # ---------------------------------------------------------
    # Go to OTP verification page
    # ---------------------------------------------------------

    return redirect(
        "verify-phone-otp"
    )

def verify_phone_otp(request):

    error = None

    # ---------------------------------------------------------
    # Get phone number stored when OTP was requested
    # ---------------------------------------------------------

    phone_number = request.session.get(
        "otp_phone_number"
    )

    if not phone_number:

        return redirect(
            "phone-login"
        )

    # ---------------------------------------------------------
    # Process OTP submission
    # ---------------------------------------------------------

    if request.method == "POST":

        entered_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        if not entered_otp:

            error = "Please enter the verification code."

        else:

            # -------------------------------------------------
            # Find the latest OTP
            # -------------------------------------------------

            otp_record = PhoneOTP.objects.filter(
                phone_number=phone_number,
                is_verified=False
            ).order_by(
                "-created_at"
            ).first()

            # -------------------------------------------------
            # No OTP found
            # -------------------------------------------------

            if not otp_record:

                error = (
                    "No active verification code was found. "
                    "Please request a new OTP."
                )

            # -------------------------------------------------
            # Check expiry
            # -------------------------------------------------

            elif timezone.now() > otp_record.expires_at:

                error = (
                    "This verification code has expired. "
                    "Please request a new OTP."
                )

                otp_record.delete()

            # -------------------------------------------------
            # Check number of attempts
            # -------------------------------------------------

            elif otp_record.attempts >= 5:

                error = (
                    "Too many incorrect attempts. "
                    "Please request a new OTP."
                )

                otp_record.delete()

            # -------------------------------------------------
            # Check OTP
            # -------------------------------------------------

            elif entered_otp != otp_record.otp:

                otp_record.attempts += 1

                otp_record.save(
                    update_fields=["attempts"]
                )

                remaining = 5 - otp_record.attempts

                error = (
                    "Incorrect verification code. "
                    f"You have {remaining} attempt(s) remaining."
                )

            # -------------------------------------------------
            # OTP is correct
            # -------------------------------------------------

            else:

                otp_record.is_verified = True

                otp_record.save(
                    update_fields=["is_verified"]
                )

                # ---------------------------------------------
                # Find the member
                # ---------------------------------------------

                member = Member.objects.filter(
                    phone_number=phone_number,
                    is_active=True
                ).first()

                if not member:

                    error = (
                        "Your member account could not be found. "
                        "Please contact the church office."
                    )

                elif not member.user:

                    error = (
                        "Your member profile is not linked "
                        "to a login account. Please contact "
                        "the church office."
                    )

                else:

                    # -----------------------------------------
                    # Log the user in
                    # -----------------------------------------

                    login(
                        request,
                        member.user
                    )

                    # -----------------------------------------
                    # Remove OTP session information
                    # -----------------------------------------

                    request.session.pop(
                        "otp_phone_number",
                        None
                    )

                    # -----------------------------------------
                    # Redirect according to account type
                    # -----------------------------------------

                    if member.user.is_superuser:

                        return redirect(
                            "/administration/dashboard/"
                        )

                    elif member.user.is_staff:

                        return redirect(
                            "/staff/"
                        )

                    else:

                        return redirect(
                            "/members/dashboard/"
                        )

    # ---------------------------------------------------------
    # Display verification page
    # ---------------------------------------------------------

    return render(

        request,

        "members/verify_phone_otp.html",

        {
            "error": error,
            "phone_number": phone_number,
        }

    )

@login_required
def member_dashboard(request):

    # ---------------------------------------------------------
    # Get the Member profile linked to this User
    # ---------------------------------------------------------

    member = getattr(
        request.user,
        "member",
        None
    )


    # ---------------------------------------------------------
    # Profile completion
    # ---------------------------------------------------------

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
            1 for field in fields
            if field
        )

        if total > 0:

            completion = int(
                (completed / total) * 100
            )


    # ---------------------------------------------------------
    # Notifications
    # ---------------------------------------------------------

    notifications = request.user.notifications.order_by(
        "-created_at"
    )[:5]


    # ---------------------------------------------------------
    # Latest pastoral follow-up
    # ---------------------------------------------------------

    latest_followup = MemberFollowUp.objects.filter(
        member=request.user
    ).order_by(
        "-created_at"
    ).first()


    # ---------------------------------------------------------
    # Unread notifications
    # ---------------------------------------------------------

    unread_notifications = MemberNotification.objects.filter(
        member=request.user,
        is_read=False
    ).count()


    # ---------------------------------------------------------
    # Latest published sermon
    # ---------------------------------------------------------

    latest_sermon = Sermon.objects.filter(
        is_published=True
    ).order_by(
        "-created_at"
    ).first()


    # ---------------------------------------------------------
    # Render dashboard
    # ---------------------------------------------------------

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

            # ==================================================
            # GET CLEANED DATA
            # ==================================================

            phone = form.cleaned_data["phone_number"]

            email = form.cleaned_data.get(
                "email"
            )

            password = form.cleaned_data["password"]


            # ==================================================
            # DETERMINE USERNAME
            # ==================================================
            #
            # If the member has an email:
            #
            #     username = email
            #
            # If the member has no email:
            #
            #     username = phone
            #
            # This allows both types of members to have
            # login accounts.
            # ==================================================

            if email:

                username = email

            else:

                username = phone


            # ==================================================
            # EXTRA SAFETY CHECK
            # ==================================================

            if User.objects.filter(
                username=username
            ).exists():

                form.add_error(
                    None,
                    "An account already exists for this "
                    "member. Please use the login option."
                )

                return render(
                    request,
                    "members/register.html",
                    {
                        "form": form
                    }
                )


            # ==================================================
            # CREATE USER ACCOUNT
            # ==================================================

            user = User.objects.create_user(

                username=username,

                email=email or "",

                password=password

            )


            # ==================================================
            # CREATE MEMBER PROFILE
            # ==================================================

            member = form.save(
                commit=False
            )

            member.user = user

            member.save()


            # ==================================================
            # ASSIGN PASTOR FOR FOLLOW-UP
            # ==================================================

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
                        "Welcome the new member, introduce them "
                        "to the church, encourage participation "
                        "in worship services, Bible study and "
                        "ministries."
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
                        "has been assigned to welcome and "
                        "support you. You may be contacted "
                        "soon for pastoral follow-up."
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
                        "Church family. Your registration has "
                        "been received successfully. A pastor "
                        "will be assigned to you shortly."
                    )

                )


            # ==================================================
            # STORE PHONE IN SESSION
            # ==================================================
            #
            # We keep the phone temporarily so the next step
            # can start the OTP verification process.
            # ==================================================

            # request.session[
            request.session[
                "otp_phone_number"
            ] = phone


            # Generate OTP immediately

            otp = str(
                random.randint(
                    100000,
                    999999
                )
            )


            # Remove old OTP

            PhoneOTP.objects.filter(
                phone_number=phone,
                is_verified=False
            ).delete()



            # Save new OTP

            PhoneOTP.objects.create(

                phone_number=phone,

                otp=otp,
                
                expires_at=timezone.now() + timedelta(minutes=5)

            )



            # Development testing only

            print(
                "======================================"
            )

            print(
                f"MPC REGISTRATION OTP for {phone}: {otp}"
            )

            print(
                "======================================"
            )



            messages.success(
                request,
                (
                    "Your account has been created. "
                    "Enter the OTP sent to your phone."
                )
            )


            return redirect(
                "verify-phone-otp"
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

    # ---------------------------------------------------------
    # Get existing Member profile if one exists
    # ---------------------------------------------------------

    member = getattr(
        user,
        "member",
        None
    )

    # ---------------------------------------------------------
    # If this is a newly created Google account and there is
    # no Member profile yet, prepare a new Member object.
    # ---------------------------------------------------------

    if member is None:

        member = Member(
            user=user,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            email=user.email or "",
        )

    # ---------------------------------------------------------
    # POST - Save profile
    # ---------------------------------------------------------

    if request.method == "POST":

        form = MemberProfileForm(
            request.POST,
            request.FILES,
            instance=member
        )

        if form.is_valid():

            # Save Member profile
            member = form.save(commit=False)

            # Make absolutely sure the Member is linked
            # to the currently authenticated User.
            member.user = user

            # Keep names synchronized
            member.first_name = request.POST.get(
                "first_name",
                member.first_name
            )

            member.last_name = request.POST.get(
                "last_name",
                member.last_name
            )

            # Keep email synchronized
            member.email = (
                request.POST.get(
                    "email",
                    user.email
                )
                or user.email
            )

            member.save()

            # -------------------------------------------------
            # Update User information
            # -------------------------------------------------

            user.first_name = (
                request.POST.get(
                    "first_name",
                    user.first_name
                )
            )

            user.last_name = (
                request.POST.get(
                    "last_name",
                    user.last_name
                )
            )

            # Email from Google should normally be preserved.
            # Only update it if a value was submitted.
            submitted_email = request.POST.get("email")

            if submitted_email:
                user.email = submitted_email

            # -------------------------------------------------
            # Profile photo
            # -------------------------------------------------

            if request.FILES.get("profile_photo"):

                user.profile_photo = request.FILES[
                    "profile_photo"
                ]

            user.save()

            # -------------------------------------------------
            # Return to dashboard
            # -------------------------------------------------

            return redirect(
                "/members/dashboard/"
            )

    # ---------------------------------------------------------
    # GET - Display profile form
    # ---------------------------------------------------------

    else:

        form = MemberProfileForm(
            instance=member
        )

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------

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