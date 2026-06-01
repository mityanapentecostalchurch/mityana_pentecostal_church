from django.contrib import admin
from .models import Sermon


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'preacher',
        'sermon_date',
        'is_published'
    )

    list_filter = (
        'is_published',
        'sermon_date'
    )

    search_fields = (
        'title',
        'preacher',
        'bible_text'
    )