from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
from videocontent.tasks import convert_480p, convert_720p, convert_1080p
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video wurde gespeichert")
    if created:
        print("Neues Video erstellt")
        queue = django_rq.get_queue("default", autocommit=True)
        queue.enqueue(convert_480p, instance.pk)
        queue.enqueue(convert_720p, instance.pk)
        queue.enqueue(convert_1080p, instance.pk)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    video_files = [
        instance.video_file,
        instance.video_file_480p,
        instance.video_file_720p,
        instance.video_file_1080p,
    ]

    for video_file in video_files:
        if video_file:
            if os.path.isfile(video_file.path):
                os.remove(video_file.path)
