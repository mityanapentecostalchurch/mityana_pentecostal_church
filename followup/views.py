from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth.decorators import login_required

from .models import MemberFollowUp


@login_required
def followup_queue(request):

    followups = MemberFollowUp.objects.filter(
        assigned_to=request.user
    ).order_by(
        'status',
        '-created_at'
    )

    return render(
        request,
        'followup/queue.html',
        {
            'followups': followups
        }
    )


@login_required
def followup_detail(request, followup_id):

    followup = MemberFollowUp.objects.get(
        id=followup_id
    )

    return render(
        request,
        'followup/detail.html',
        {
            'followup': followup
        }
    )


@login_required
def complete_followup(request, followup_id):

    followup = MemberFollowUp.objects.get(
        id=followup_id
    )

    followup.status = 'COMPLETED'

    followup.save()

    return redirect(
        f'/followup/{followup.id}/'
    )


@login_required
def update_notes(request, followup_id):

    followup = MemberFollowUp.objects.get(
        id=followup_id
    )

    if request.method == "POST":

        followup.pastor_notes = request.POST.get(
            "pastor_notes"
        )

        followup.save()

    return redirect(
        f'/followup/{followup.id}/'
    )

@login_required
def schedule_visit(request, followup_id):

    followup = MemberFollowUp.objects.get(
        id=followup_id
    )

    if request.method == "POST":

        followup.visit_required = True

        followup.visit_type = request.POST.get(
            "visit_type"
        )

        followup.visit_date = request.POST.get(
            "visit_date"
        )

        followup.visit_time = request.POST.get(
            "visit_time"
        )

        followup.visit_location = request.POST.get(
            "visit_location"
        )

        followup.save()

        return redirect(
            f'/followup/{followup.id}/'
        )

    return render(

        request,

        'followup/schedule_visit.html',

        {

            'followup': followup

        }

    )

@login_required
def complete_visit(request, followup_id):

    followup = MemberFollowUp.objects.get(
        id=followup_id
    )

    followup.visit_completed = True

    followup.save()

    return redirect(
        f'/followup/{followup.id}/'
    )