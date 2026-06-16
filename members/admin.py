# members/admin.py

from django.contrib import admin
# from .models import Member
from .models import (Member, Department, Role)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'department',
        'role',
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
        'department',
        'role',
        'status',
        'is_active',
    )

    fieldsets = (

        ("User Account", {
            'fields': (
                'user',
            )
        }),

        ("Personal Information", {
            'fields': (
                'first_name',
                'last_name',
                'gender',
                'birthday',
            )
        }),

        ("Contact Information", {
            'fields': (
                'phone_number',
                'whatsapp_number',
                'email',
            )
        }),

        ("Residence Information", {
            'fields': (
                'address',
                'village',
                'parish',
                'sub_county',
                'district',
            )
        }),

        ("Family Information", {
            'fields': (
                'marital_status',
                'number_of_children',
                'next_of_kin',
                'next_of_kin_contact',
            )
        }),

        ("Employment & Education", {
            'fields': (
                'occupation',
                'employer',
                'place_of_work',
                'education_level',
                'is_student',
                'school_name',
            )
        }),

        ("Housing", {
            'fields': (
                'is_renting',
                'landlord_name',
            )
        }),

        ("Salvation & Baptism", {
            'fields': (
                'date_saved',
                'church_where_saved',
                'is_baptized',
                'baptism_date',
                'baptism_place',
            )
        }),

        ("Church Background", {
            'fields': (
                'former_church',
                'former_pastor',
                'previous_ministry',
            )
        }),

        ("Ministry Information", {
            'fields': (
                'department',
                'role',
                'desired_ministry',
                'years_at_mpc',
                'date_joined',
                'status',
                'is_active',
            )
        }),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'leader',
    )

    search_fields = (
        'name',
    )