from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'member',
        'service_date',
        'status'
    )

    list_filter = (
        'service_date',
        'status'
    )

    search_fields = (
        'member__first_name',
        'member__last_name'
    )