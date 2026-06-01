from django.shortcuts import render
from announcements.models import Announcement


def home(request):

    announcements = Announcement.objects.filter(
        is_active=True
    )[:5]

    context = {
        'announcements': announcements
    }

    return render(
        request,
        'home.html',
        context
    )


def about(request):
    return render(request, 'about.html')


def leadership(request):
    return render(request, 'leadership.html')


def contact(request):
    return render(request, 'contact.html')