from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Contribution,
    ContributionCategory
)


@admin.register(ContributionCategory)
class ContributionCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):

    list_display = (
        'member',
        'category',
        'amount',
        'payment_method',
        'contribution_date',
    )

    search_fields = (
        'member__first_name',
        'member__last_name',
        'reference_number',
    )

    list_filter = (
        'payment_method',
        'category',
        'contribution_date',
    )