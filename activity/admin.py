from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'action',
        'created_at',
    )

    list_filter = (
        'user',
        'created_at',
    )

    search_fields = (
        'action',
    )

    ordering = (
        '-created_at',
    )