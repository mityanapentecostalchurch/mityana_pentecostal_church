from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.decorators import login_required

from .forms import PrayerRequestForm
from .models import PrayerRequest


@login_required
def create_prayer_request(request):

    if request.method == 'POST':

        form = PrayerRequestForm(
            request.POST
        )

        if form.is_valid():

            prayer = form.save(
                commit=False
            )

            prayer.member = request.user

            prayer.save()

            return redirect(
                '/members/dashboard/'
            )

    else:

        form = PrayerRequestForm()

    return render(
        request,
        'prayers/create.html',
        {
            'form': form
        }
    )
@login_required
def my_prayer_requests(request):

    requests = PrayerRequest.objects.filter(
        member=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'prayers/list.html',
        {
            'requests': requests
        }
    )