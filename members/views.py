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

                return redirect('/admin/')

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

    return render(
        request,
        'members/dashboard.html',
        {
            'member': member,
            'completion': completion,
        }
    )

def member_register(request):

    if request.method == "POST":

        form = MemberRegistrationForm(
            request.POST
        )

        if form.is_valid():

            email = form.cleaned_data[
                'email'
            ]

            password = form.cleaned_data[
                'password'
            ]

            if User.objects.filter(
                email=email
            ).exists():

                form.add_error(
                    'email',
                    'An account with this email already exists.'
                )

            else:

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                member = form.save(
                    commit=False
                )

                member.user = user

                member.save()

                login(
                    request,
                    user
                )

                # return redirect('/')
                return redirect(
                    '/members/dashboard/')

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

    if request.method == 'POST':

        form = MemberProfileForm(
            request.POST,
            instance=member
        )

        if form.is_valid():

            form.save()

            return redirect(
                '/members/dashboard/'
            )

    else:

        form = MemberProfileForm(
            instance=member
        )

    return render(
        request,
        'members/edit_profile.html',
        {
            'form': form
        }
    )
def member_logout(request):

    logout(request)

    return redirect('/')

@login_required
def change_password(request):

    if request.method == 'POST':

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

            return redirect('/')

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'members/change_password.html',
        {
            'form': form
        }
    )



@login_required
def notifications(request):

    counselling = CounsellingRequest.objects.filter(
        member=request.user,
        status='SCHEDULED'
    ).order_by('-created_at')

    return render(
        request,
        'members/notifications.html',
        {
            'counselling': counselling
        }
    )