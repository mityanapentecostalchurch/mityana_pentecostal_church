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
from prayers.models import (
    PrayerRequest,
    PrayerNote
)
from django.utils import timezone
# from prayers.models import PrayerNote
from django.contrib import messages

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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:

                login(
                    request,
                    user
                )

                return redirect(
                    '/staff/'
                )

            else:

                error = (
                    "This account is not a staff account."
                )

        else:

            error = (
                "Invalid username or password."
            )

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

@login_required
def prayer_detail(request, prayer_id):

    prayer = PrayerRequest.objects.get(
        id=prayer_id
    )

    notes = prayer.notes.all()

    return render(
        request,
        'staff/prayer_detail.html',
        {
            'prayer': prayer,
            'notes': notes,
        }
    )

@login_required
def mark_prayed(request, prayer_id):

    prayer = PrayerRequest.objects.get(
        id=prayer_id
    )

    prayer.status = 'PRAYED'

    prayer.prayed_by = request.user.username

    prayer.prayed_at = timezone.now()

    prayer.save()

    return redirect(
        f'/staff/prayers/{prayer.id}/'
    )

@login_required
def add_prayer_note(request, prayer_id):

    prayer = PrayerRequest.objects.get(
        id=prayer_id
    )

    if request.method == "POST":

        note = request.POST.get("note")

        if note and note.strip():

            PrayerNote.objects.create(

                prayer=prayer,

                staff=request.user,

                note=note.strip()

            )

        return redirect(
            f'/staff/prayers/{prayer.id}/'
        )

    messages.success(
        request,
        "Prayer note saved successfully."
        )
    return redirect(
        f'/staff/prayers/{prayer.id}/'
        
    )

@login_required
def edit_prayer_note(request, note_id):

    note = PrayerNote.objects.get(
        id=note_id
    )

    if request.method == "POST":

        note.note = request.POST.get(
            "note"
        )

        note.save()

        return redirect(
            f'/staff/prayers/{note.prayer.id}/'
        )

    return render(
        request,
        'staff/edit_note.html',
        {
            'note': note
        }
    )

@login_required
def delete_prayer_note(request, note_id):

    note = PrayerNote.objects.get(
        id=note_id
    )

    prayer_id = note.prayer.id

    note.delete()

    return redirect(
        f'/staff/prayers/{prayer_id}/'
    )