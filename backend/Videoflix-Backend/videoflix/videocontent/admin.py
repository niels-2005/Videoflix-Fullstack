from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class VideoAdmin(ImportExportModelAdmin):
    list_display = (
        "title",
        "created_at",
        "description",
    )  # Diese Felder werden in der Listenansicht angezeigt
    fields = (
        "title",
        "created_at",
        "description",
        "video_file",
    )  # Diese Felder können bearbeitet werden


admin.site.register(Video, VideoAdmin)


class VideoResource(resources.ModelResource):
    class Meta:
        model = Video
