# members/urls.py

from django.urls import path
# from .views import member_register, member_dashboard

from .views import (
    member_register,
    member_dashboard,
    member_login,
    forgot_password,
    phone_login,
    send_phone_otp,
    verify_phone_otp,
    edit_profile,
    member_logout,
    change_password,
    notifications,

)
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        'register/',
        member_register,
        name='member-register'
    ),

    path(
        'dashboard/',
        member_dashboard,
        name='member-dashboard'
    ),

    path(
        'login/',
        member_login,
        name='member-login'
    ),
    
    path(
        "forgot-password/",
        forgot_password,
        name="forgot-password"
    ),
    # path(
    #     "password-reset/",
    #     auth_views.PasswordResetView.as_view(
    #         template_name="members/password_reset.html",
    #         email_template_name="registration/password_reset_email.html",
    #         subject_template_name="registration/password_reset_subject.txt"
    #     ),
    #     name="password_reset"
    # ),


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
            template_name="members/password_reset_confirm.html",
            success_url="/members/reset-complete/"
        ),
        name="password_reset_confirm"
    ),

    


    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="members/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
    path(
        "login/phone/",
        phone_login,
        name="phone-login"
    ),

    path(
        "login/phone/send/",
        send_phone_otp,
        name="send-phone-otp"
    ),
    path(
        "login/phone/verify/",
        verify_phone_otp,
        name="verify-phone-otp"
    ),

    path(
        'profile/edit/',
        edit_profile,
        name='edit-profile'
    ),

    path(
        'logout/',
        member_logout,
        name='member-logout'
    ),

    path(
        'change-password/',
        change_password,
        name='change-password'
    ),

    path(
        'notifications/',
        notifications,
        name='notifications'
    ),
]