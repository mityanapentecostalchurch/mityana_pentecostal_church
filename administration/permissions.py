from functools import wraps
from django.shortcuts import redirect


FULL_ADMIN_ROLES = [

    "ADMINISTRATOR",

    "PASTOR",

]


MEMBER_ROLES = [

    "ADMINISTRATOR",

    "PASTOR",

    "SECRETARY",

]


FINANCE_ROLES = [

    "ADMINISTRATOR",

    "PASTOR",

    "TREASURER",

]


SECRETARY_ROLES = [

    "ADMINISTRATOR",

    "PASTOR",

    "SECRETARY",

]

def full_admin_required(view):

    @wraps(view)

    def wrapper(request, *args, **kwargs):

        user = request.user

        if user.is_superuser:

            return view(request, *args, **kwargs)

        if user.role in FULL_ADMIN_ROLES:

            return view(request, *args, **kwargs)

        return redirect("/administration/login/")

    return wrapper

def member_management_required(view):

    @wraps(view)

    def wrapper(request, *args, **kwargs):

        user = request.user

        if user.is_superuser:

            return view(request, *args, **kwargs)

        if user.role in MEMBER_ROLES:

            return view(request, *args, **kwargs)

        return redirect("/administration/login/")

    return wrapper

def finance_required(view):

    @wraps(view)

    def wrapper(request, *args, **kwargs):

        user = request.user

        if user.is_superuser:

            return view(request, *args, **kwargs)

        if user.role in FINANCE_ROLES:

            return view(request, *args, **kwargs)

        return redirect("/administration/login/")

    return wrapper

def secretary_required(view):

    @wraps(view)

    def wrapper(request, *args, **kwargs):

        user = request.user

        if user.is_superuser:

            return view(request, *args, **kwargs)

        if user.role in SECRETARY_ROLES:

            return view(request, *args, **kwargs)

        return redirect("/administration/login/")

    return wrapper