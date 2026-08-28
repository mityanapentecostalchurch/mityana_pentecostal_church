from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    member_register,
    member_dashboard,
    member_login,
    forgot_password,
    edit_profile,
    member_logout,
    change_password,
    notifications,
)

urlpatterns = [
    path(
        "register/",
        member_register,
        name="member-register"
    ),

    path(
        "dashboard/",
        member_dashboard,
        name="member-dashboard"
    ),

    path(
        "login/",
        member_login,
        name="member-login"
    ),

    path(
        "forgot-password/",
        forgot_password,
        name="forgot-password"
    ),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="members/password_reset.html"
        ),
        name="password_reset"
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="members/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="members/password_reset_confirm.html"
        ),
        name="password_reset_confirm"
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="members/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    path(
        "profile/edit/",
        edit_profile,
        name="edit-profile"
    ),

    path(
        "logout/",
        member_logout,
        name="member-logout"
    ),

    path(
        "change-password/",
        change_password,
        name="change-password"
    ),

    path(
        "notifications/",
        notifications,
        name="notifications"
    ),
]