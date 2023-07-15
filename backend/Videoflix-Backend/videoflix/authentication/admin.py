from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
    )  # Hinzufügen von 'is_active' zur Anzeige


admin.site.unregister(User)  # UserAdmin deaktivieren
admin.site.register(User, CustomUserAdmin)  # CustomUserAdmin registrieren
