from django.shortcuts import (

    render,

    redirect,

    get_object_or_404

)

from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from .models import PastoralVisit

from followup.models import MemberNotification

User = get_user_model()


@login_required
def visit_queue(request):

    visits = PastoralVisit.objects.filter(

        pastor=request.user

    ).order_by(

        'visit_date'

    )

    return render(

        request,

        'visitations/queue.html',

        {

            'visits': visits

        }

    )


@login_required
def new_visit(request):

    members = User.objects.filter(

        role='MEMBER'

    )

    if request.method == "POST":

        member = User.objects.get(

            id=request.POST.get("member")

        )

        visit = PastoralVisit.objects.create(

            member=member,

            pastor=request.user,

            visit_type=request.POST.get("visit_type"),

            visit_date=request.POST.get("visit_date"),

            visit_time=request.POST.get("visit_time"),

            location=request.POST.get("location"),

            purpose=request.POST.get("purpose")

        )

        MemberNotification.objects.create(

            member=member,

            title="Pastoral Visit Scheduled",

            message=f"A {visit.get_visit_type_display()} has been scheduled for {visit.visit_date} at {visit.visit_time}."

        )

        return redirect("/visitations/")

    return render(

        request,

        'visitations/new_visit.html',

        {

            'members': members

        }

    )


@login_required
def visit_detail(request, visit_id):

    visit = get_object_or_404(

        PastoralVisit,

        id=visit_id

    )

    if request.method == "POST":

        visit.notes = request.POST.get(

            "notes"

        )

        visit.save()

        MemberNotification.objects.create(

            member=visit.member,

            title="Visit Updated",

            message=(
                "Your pastoral visit record has been updated. "
                "If you have any questions, please contact your pastor."
            )

        )

    return render(

        request,

        'visitations/detail.html',

        {

            'visit': visit

        }

    )


@login_required
def complete_visit(request, visit_id):

    visit = get_object_or_404(

        PastoralVisit,

        id=visit_id

    )

    visit.status = "COMPLETED"

    visit.save()

    MemberNotification.objects.create(

        member=visit.member,

        title="Visit Completed",

        message="Your pastoral visit has been completed. May God continue to bless and strengthen you."

    )

    return redirect(

        f"/visitations/{visit.id}/"

    )