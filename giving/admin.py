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
        'contribution_date'
    )

    list_filter = (
        'category',
        'payment_method'
    )

    search_fields = (
        'reference_number',
    )