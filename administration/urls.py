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
        "departments/",
        views.departments,
        name="admin-departments"
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
]