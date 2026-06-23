from django.contrib import admin
from .models import PrayerRequest


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):

    list_display = (

        'title',

        'member',

        'status',

        'prayed_by',

        'created_at',

    )

    list_filter = (

        'status',

        'created_at',

    )

    search_fields = (

        'title',

        'member__username',

    )