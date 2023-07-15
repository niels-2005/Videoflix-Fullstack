from django.db import transaction
from .models import Video
from django.conf import settings
import subprocess
import os


@transaction.atomic
def convert_480p(video_pk):
    video = Video.objects.get(pk=video_pk)
    source = video.video_file.path
    target = source + "_480p.mp4"
    cmd = (
        'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source, target
        )
    )
    subprocess.run(cmd, shell=True)
    relative_target = os.path.relpath(target, settings.MEDIA_ROOT)
    video.video_file_480p.name = relative_target
    video.save()


@transaction.atomic
def convert_720p(video_pk):
    video = Video.objects.get(pk=video_pk)
    source = video.video_file.path
    target = source + "_720p.mp4"
    cmd = (
        'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source, target
        )
    )
    subprocess.run(cmd, shell=True)
    relative_target = os.path.relpath(target, settings.MEDIA_ROOT)
    video.video_file_720p.name = relative_target
    video.save()


@transaction.atomic
def convert_1080p(video_pk):
    video = Video.objects.get(pk=video_pk)
    source = video.video_file.path
    target = source + "_1080p.mp4"
    cmd = (
        'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(
            source, target
        )
    )
    subprocess.run(cmd, shell=True)
    relative_target = os.path.relpath(target, settings.MEDIA_ROOT)
    video.video_file_1080p.name = relative_target
    video.save()
