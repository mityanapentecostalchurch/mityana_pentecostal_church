from prayers.models import PrayerRequest

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
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
from members.models import Member

from prayers.models import PrayerRequest

from counselling.models import CounsellingRequest

from followup.models import MemberFollowUp

from visitations.models import PastoralVisit

from followup.models import MemberNotification
from sermons.models import Sermon
from accounts.models import User
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from accounts.cloudinary_utils import upload_profile_photo


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
                    'staff-dashboard'
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
    published_sermons = Sermon.objects.filter(
        is_published=True
    ).count()

    draft_sermons = Sermon.objects.filter(
        is_published=False
    ).count()

    this_month_sermons = Sermon.objects.filter(
        sermon_date__month=timezone.now().month,
        sermon_date__year=timezone.now().year
    ).count()

    return render(
        request,
        'staff/dashboard.html',
        {
            'user': request.user,
            'published_sermons': published_sermons,

            'draft_sermons': draft_sermons,

            'this_month_sermons': this_month_sermons,

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

@login_required
def member_list(request):

    search = request.GET.get("search")

    members = Member.objects.all()

    if search:

        members = members.filter(

            first_name__icontains=search

        ) | members.filter(

            last_name__icontains=search

        )

    return render(

        request,

        "staff/member_list.html",

        {

            "members": members,

            "search": search

        }

    )

@login_required
def member_profile(request, member_id):

    member = get_object_or_404(

        Member,

        id=member_id

    )

    prayers = PrayerRequest.objects.filter(

        member=member.user

    ).order_by("-created_at")

    counselling = CounsellingRequest.objects.filter(

        member=member.user

    ).order_by("-created_at")

    followups = MemberFollowUp.objects.filter(

        member=member.user

    ).order_by("-created_at")

    visits = PastoralVisit.objects.filter(

        member=member.user

    ).order_by("-visit_date")

    notifications = MemberNotification.objects.filter(

        member=member.user

    ).order_by("-created_at")[:10]

    return render(

        request,

        "staff/member_profile.html",

        {

            "member": member,

            "prayers": prayers,

            "counselling": counselling,

            "followups": followups,

            "visits": visits,

            "notifications": notifications,

        }

    )
@login_required
def staff_sermons(request):

    sermons = Sermon.objects.all().order_by(
        '-sermon_date'
    )

    return render(

        request,

        'staff/sermons.html',

        {

            'sermons': sermons,

            'total_sermons': sermons.count(),

            'published_sermons': sermons.filter(
                is_published=True
            ).count(),

            'draft_sermons': sermons.filter(
                is_published=False
            ).count(),

        }

    )



@login_required
def new_sermon(request):

    if request.method == "POST":

        sermon = Sermon.objects.create(

            title=request.POST.get("title"),

            preacher=request.POST.get("preacher"),

            bible_text=request.POST.get("bible_text"),

            sermon_date=request.POST.get("sermon_date"),

            summary=request.POST.get("summary"),

            youtube_link=request.POST.get("youtube_link"),

            featured_image=request.FILES.get(
                "featured_image"
            ),

            pdf_notes=request.FILES.get(
                "pdf_notes"
            ),

            audio_file=request.FILES.get(
                "audio_file"
            ),

            is_published=(
                request.POST.get("is_published") == "on"
            )

        )

        # Notify church members

        if sermon.is_published:

            members = User.objects.filter(
                role="MEMBER"
            )

            notifications = []

            for member in members:

                notifications.append(

                    MemberNotification(

                        member=member,

                        title=" New Sermon Available",

                        message=(
                            f'"{sermon.title}" by '
                            f'{sermon.preacher} '
                            f'is now available. '
                            "Visit the Sermons page to read, "
                            "watch or download it."
                        )

                    )

                )

            MemberNotification.objects.bulk_create(
                notifications
            )

        messages.success(

            request,

            "Sermon has been saved successfully."

        )

        return redirect(
            "/staff/sermons/"
        )

    return render(

        request,

        "staff/new_sermon.html"

    )

@login_required
def edit_sermon(request, sermon_id):

    sermon = get_object_or_404(
        Sermon,
        id=sermon_id
    )

    if request.method == "POST":

        sermon.title = request.POST.get("title")

        sermon.preacher = request.POST.get("preacher")

        sermon.bible_text = request.POST.get(
            "bible_text"
        )

        sermon.sermon_date = request.POST.get(
            "sermon_date"
        )

        sermon.summary = request.POST.get(
            "summary"
        )

        sermon.youtube_link = request.POST.get(
            "youtube_link"
        )

        if request.FILES.get(
            "featured_image"
        ):
            sermon.featured_image = request.FILES.get(
                "featured_image"
            )

        if request.FILES.get(
            "pdf_notes"
        ):
            sermon.pdf_notes = request.FILES.get(
                "pdf_notes"
            )

        if request.FILES.get(
            "audio_file"
        ):
            sermon.audio_file = request.FILES.get(
                "audio_file"
            )

        sermon.is_published = (
            request.POST.get(
                "is_published"
            ) == "on"
        )

        sermon.save()

        return redirect(
            "/staff/sermons/"
        )

    return render(

        request,

        "staff/edit_sermon.html",

        {

            "sermon": sermon

        }

    )

@login_required
def delete_sermon(request, sermon_id):

    sermon = get_object_or_404(

        Sermon,

        id=sermon_id

    )

    sermon.delete()

    return redirect(
        "/staff/sermons/"
    )
@login_required
def staff_profile(request):

    return render(

        request,

        "staff/profile.html",

        {

            "user": request.user

        }

    )


@login_required
def edit_staff_profile(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get(
            "first_name"
        )

        user.last_name = request.POST.get(
            "last_name"
        )

        user.email = request.POST.get(
            "email"
        )

        user.phone_number = request.POST.get(
            "phone_number"
        )

        user.position = request.POST.get(
            "position"
        )

        user.office = request.POST.get(
            "office"
        )

        user.department = request.POST.get(
            "department"
        )

        user.biography = request.POST.get(
            "biography"
        )

        # if request.FILES.get("profile_photo"):

        #     user.profile_photo = request.FILES.get(
        #         "profile_photo"
        #     )
        if request.FILES.get("profile_photo"):

            photo = request.FILES.get("profile_photo")

            result = upload_profile_photo(photo)

            user.profile_photo = result["public_id"]

        user.save()

        messages.success(

            request,

            "Profile updated successfully."

        )

        return redirect(
            "staff-profile"
        )

    return render(

        request,

        "staff/edit_profile.html",

        {

            "user": user

        }

    )

