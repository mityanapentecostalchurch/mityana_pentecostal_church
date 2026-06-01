from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def leadership(request):
    return render(request, 'leadership.html')


def contact(request):
    return render(request, 'contact.html')