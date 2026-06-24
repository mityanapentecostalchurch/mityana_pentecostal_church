from django.shortcuts import render

# Create your views here.
from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.decorators import login_required

from .forms import (
    CounsellingRequestForm
)

from .models import (
    CounsellingRequest
)

from accounts.models import User
from django.core.mail import send_mail


@login_required
def new_counselling_request(request):

    if request.method == 'POST':

        form = CounsellingRequestForm(
            request.POST
        )

        if form.is_valid():

            counselling = form.save(
                commit=False
            )

            counselling.member = (
                request.user
            )

            pastor = User.objects.filter(
                role='PASTOR'
            ).first()

            if pastor:

                counselling.assigned_to = (
                    pastor
                )

            counselling.save()

            return redirect(
                '/members/dashboard/'
            )

    else:

        form = CounsellingRequestForm()

    return render(
        request,
        'counselling/new_request.html',
        {
            'form': form
        }
    )

@login_required
def counselling_queue(request):

    requests = CounsellingRequest.objects.filter(
        assigned_to=request.user
    )

    return render(
        request,
        'counselling/queue.html',
        {
            'requests': requests
        }
    )

@login_required
def my_counselling_requests(request):

    requests = CounsellingRequest.objects.filter(
        member=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'counselling/my_requests.html',
        {
            'requests': requests
        }
    )

@login_required
def counselling_detail(request, request_id):

    counselling = CounsellingRequest.objects.get(
        id=request_id
    )

    return render(
        request,
        'counselling/detail.html',
        {
            'counselling': counselling
        }
    )

@login_required
def schedule_counselling(
    request,
    request_id
):

    counselling = CounsellingRequest.objects.get(
        id=request_id
    )

    if request.method == 'POST':

        counselling.scheduled_date = request.POST.get(
            'scheduled_date'
        )

        counselling.scheduled_time = request.POST.get(
            'scheduled_time'
        )

        counselling.location = request.POST.get(
            'location'
        )

        counselling.status = 'SCHEDULED'

        counselling.save()

        send_mail(

            'Counselling Appointment Scheduled',

            f'''
        Your counselling request "{counselling.subject}"
        has been scheduled.

        Date: {counselling.scheduled_date}

        Time: {counselling.scheduled_time}

        Location: {counselling.location}
        ''',

            'noreply@mpc.org',

            [counselling.member.email],

            fail_silently=True,

        )

        # return redirect(
        #     f'/staff/counselling/{counselling.id}/'
        # )
        return redirect(
            f'/counselling/{counselling.id}/'
        )

    return render(
        request,
        'counselling/schedule.html',
        {
            'counselling': counselling
        }
    )