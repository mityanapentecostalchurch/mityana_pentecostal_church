from django.contrib import admin

# Register your models here.
from django.contrib import admin
# from .models import Attendance
from .models import Attendance, Service


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'member',
        'service',
        'status',
        'recorded_at',
    )

    list_filter = (
        'service',
        'status',
        'member__first_name',
        'member__last_name',
    )

    search_fields = (
        'member__first_name',
        'member__last_name',
    )



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'service_type',
        'service_date'
    )

    list_filter = (
        'service_type',
    )