# members/admin.py

from django.contrib import admin
# from .models import Member
from .models import (Member, Department, Role)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'gender',
        'department',
        'role',
        'phone_number',
        'date_joined',
        'status',
        'is_active',
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone_number',
        'email',
    )

    list_filter = (
        'is_active',
        'department',
        'role',
        'status',
    )

    ordering = (
        'first_name',
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

