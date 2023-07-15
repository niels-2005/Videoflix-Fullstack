from django.db import models
from datetime import date


class Video(models.Model):
    created_at = models.DateField(default=date.today)
    created_from = models.CharField(max_length=100, default="Guest", blank=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    video_file = models.FileField(upload_to="videos", blank=True, null=True)
    video_file_480p = models.FileField(upload_to="videos", blank=True, null=True)
    video_file_720p = models.FileField(upload_to="videos", blank=True, null=True)
    video_file_1080p = models.FileField(upload_to="videos", blank=True, null=True)

    def __str__(self) -> str:
        return self.title
