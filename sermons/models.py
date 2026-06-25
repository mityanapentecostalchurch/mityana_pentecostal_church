from django.db import models


class Sermon(models.Model):

    title = models.CharField(
        max_length=255
    )

    preacher = models.CharField(
        max_length=150
    )

    bible_text = models.CharField(
        max_length=255,
        blank=True
    )

    sermon_date = models.DateField()

    summary = models.TextField()

    youtube_link = models.URLField(
        blank=True,
        null=True
    )

    featured_image = models.ImageField(
        upload_to='sermons/images/',
        blank=True,
        null=True
    )

    pdf_notes = models.FileField(
        upload_to='sermons/pdfs/',
        blank=True,
        null=True
    )

    audio_file = models.FileField(
        upload_to='sermons/audio/',
        blank=True,
        null=True
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            '-sermon_date'
        ]

    def __str__(self):

        return self.title