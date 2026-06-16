from django.contrib import admin
from .models import ChurchLeader

@admin.register(ChurchLeader)
class ChurchLeaderAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'position',
        'phone_number',
        'is_active',
    )

    search_fields = (
        'full_name',
    )