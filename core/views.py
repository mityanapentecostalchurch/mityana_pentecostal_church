from django.shortcuts import render
from announcements.models import Announcement
from events.models import Event
from sermons.models import Sermon
from accounts.models import User
# from sermons.models import Sermon

# def home(request):

#     announcements = Announcement.objects.filter(
#         is_active=True
#     )[:5]

#     context = {
#         'announcements': announcements
#     }

#     return render(
#         request,
#         'home.html',
#         context
#     )

def home(request):

    announcements = Announcement.objects.filter(
        is_active=True
    )[:5]

    events = Event.objects.filter(
        is_active=True
    )[:5]

    sermons = Sermon.objects.filter(
        is_published=True
    )[:3]

    context = {
        'announcements': announcements,
        'events': events,
        'sermons': sermons
    }

    return render(
        request,
        'home.html',
        context
    )

def about(request):
    return render(request, 'about.html')



def leadership(request):

    leaders = User.objects.filter(

        role__in=[

            "PASTOR",

            "SECRETARY",

            "TREASURER",

            "MINISTRY_LEADER",

            "INTERCESSOR",

            "SUPER_ADMIN",

        ]

    )

    print("LEADERS FOUND:", leaders.count())

    for leader in leaders:
        print(
            leader.first_name,
            leader.role
        )

    return render(

        request,

        "leadership.html",

        {

            "leaders": leaders

        }

    )

def contact(request):
    return render(request, 'contact.html')

# def sermons(request):

#     sermons = Sermon.objects.filter(
#         is_published=True
#     )

#     return render(
#         request,
#         'sermons.html',
#         {
#             'sermons': sermons
#         }
#     )

def sermon_list(request):

    sermons = Sermon.objects.filter(
        is_published=True
    )

    return render(
        request,
        'sermons.html',
        {
            'sermons': sermons
        }
    )
def announcement_list(request):

    announcements = Announcement.objects.filter(
        is_active=True
    )

    return render(
        request,
        'announcements.html',
        {
            'announcements': announcements
        }
    )


def event_list(request):

    events = Event.objects.filter(
        is_active=True
    )

    return render(
        request,
        'events.html',
        {
            'events': events
        }
    )

def services(request):

    return render(
        request,
        'services.html'
    )

def ministries(request):

    return render(
        request,
        'ministries.html'
    )

