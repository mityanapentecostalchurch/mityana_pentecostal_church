from prayers.models import PrayerRequest
from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
)

STAFF_ROLES = [

    'SUPER_ADMIN',
    'PASTOR',
    'SECRETARY',
    'TREASURER',
    'MINISTRY_LEADER',
    'INTERCESSOR',

]


def staff_login(request):

    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME:", username)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("USER:", user)

        if user is not None:

            print("USER TYPE:", user.user_type)
            print("ROLE:", user.role)

            if user.user_type == 'STAFF':

                login(request, user)

                return redirect('/staff/')

            else:

                error = "This account is not staff."

        else:

            error = "Invalid username or password."

    return render(
        request,
        'staff/login.html',
        {
            'error': error
        }
    )

@login_required
def staff_dashboard(request):

    # if request.user.user_type != 'STAFF':
    if not request.user.is_staff:

        return redirect(
            '/members/dashboard/'
        )

    return render(
        request,
        'staff/dashboard.html',
        {
            'user': request.user
        }
    )



@login_required
def prayer_queue(request):

    prayers = PrayerRequest.objects.filter(
        assigned_to=request.user
    )

    return render(
        request,
        'staff/prayers.html',
        {
            'prayers': prayers
        }
    )