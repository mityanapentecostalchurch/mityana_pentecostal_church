from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (

        (
            'Church Information',
            {
                'fields': (

                    'phone_number',
                    'user_type',
                    'role',

                )
            }
        ),

    )

    list_display = (

        'username',
        'email',
        'first_name',
        'last_name',
        'user_type',
        'role',
        'is_staff',

    )