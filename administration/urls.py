from django.urls import path
from . import views

urlpatterns = [

    path(
        "dashboard/",
        views.dashboard,
        name="admin-dashboard"
    ),

    path(
        "login/",
        views.admin_login,
        name="admin-login"
    ),

    path(
        "members/",
        views.members,
        name="admin-members"
    ),

    path(
        "staff/",
        views.staff,
        name="admin-staff"
    ),

    path(
        "staff/add/",
        views.add_staff,
        name="admin-add-staff"
    ),

    path(
        "staff/<int:staff_id>/",
        views.staff_details,
        name="admin-staff-details"
    ),

    path(
        "staff/<int:staff_id>/edit/",
        views.edit_staff,
        name="admin-edit-staff"
    ),

    path(
        "staff/<int:staff_id>/toggle-status/",
        views.toggle_staff_status,
        name="admin-toggle-staff-status"
    ),


   
    path(
        "departments/",
        views.departments,
        name="admin-departments"
    ),

    path(
        "departments/add/",
        views.add_department,
        name="admin-add-department"
    ),

    path(
        "departments/<int:department_id>/",
        views.department_details,
        name="admin-department-details"
    ),

    path(
        "departments/<int:department_id>/edit/",
        views.edit_department,
        name="admin-edit-department"
    ),

    path(
        "departments/<int:department_id>/delete/",
        views.delete_department,
        name="admin-delete-department"
    ),

    path(
        "events/",
        views.events,
        name="admin-events"
    ),

    path(
        "announcements/",
        views.announcements,
        name="admin-announcements"
    ),

    path(
        "prayers/",
        views.prayers,
        name="admin-prayers"
    ),

    path(
        "counselling/",
        views.counselling,
        name="admin-counselling"
    ),

    path(
        "giving/",
        views.giving,
        name="admin-giving"
    ),

    path(
        "reports/",
        views.reports,
        name="admin-reports"
    ),

    path(
        "settings/",
        views.settings,
        name="admin-settings"
    ),

    path(
        "members/<int:member_id>/",
        views.member_details,
        name="admin-member-details",
    ),

    path(
        "members/<int:member_id>/edit/",
        views.edit_member,
        name="admin-edit-member"
    ),
]