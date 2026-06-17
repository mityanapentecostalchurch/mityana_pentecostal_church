# members/views.py

from django.shortcuts import (
    render,
    redirect,
)

from django.contrib.auth import (
    get_user_model,
    login,
)

from .forms import (
    MemberRegistrationForm
)

from django.contrib.auth.decorators import login_required


User = get_user_model()

@login_required
def member_dashboard(request):

    # member = request.user.member
    try:
        member = request.user.member
    except Exception:
        member = None
    

    return render(
        request,
        'members/dashboard.html',
        {
            'member': member
        }
    )

def member_register(request):

    if request.method == "POST":

        form = MemberRegistrationForm(
            request.POST
        )

        if form.is_valid():

            email = form.cleaned_data[
                'email'
            ]

            password = form.cleaned_data[
                'password'
            ]

            if User.objects.filter(
                email=email
            ).exists():

                form.add_error(
                    'email',
                    'An account with this email already exists.'
                )

            else:

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

                member = form.save(
                    commit=False
                )

                member.user = user

                member.save()

                login(
                    request,
                    user
                )

                # return redirect('/')
                return redirect(
                    '/members/dashboard/')

    else:

        form = MemberRegistrationForm()

    return render(
        request,
        'members/register.html',
        {
            'form': form
        }
    )

