# from django.shortcuts import render

# Create your views here.
# members/views.py

from django.shortcuts import (
    render,
    redirect,
)

from .forms import (
    MemberRegistrationForm
)


def member_register(request):

    if request.method == "POST":

        form = MemberRegistrationForm(
            request.POST
        )

        if form.is_valid():

            member = form.save()

            return redirect('/')

    else:

        form = MemberRegistrationForm()

    return render(
        request,
        'members/register.html',
        {
            'form': form
        }
    )